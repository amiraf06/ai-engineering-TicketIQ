# TicketIQ: V1 Architecture Specification, Decisions, and Traceability

**Version:** 1.3  
**Status:** Week 2 Conceptual V1 Architecture  

---

## Step C1 - Starting with the Simplest Architecture

### 1. Baseline Simple Flow
`Support Agent Query -> TicketIQ Application -> Single AI Model Capability -> Category & Troubleshooting Response`

### 2. What the Simple Architecture Can Do
* Accepts raw support ticket text from a help-desk agent and returns a predicted category or generic troubleshooting advice based on a single model's internal parameters.
* Minimises initial setup complexity by avoiding external data stores, pre-processing filters, and post-processing verification gates.

### 3. Why the Simple Architecture Fails TicketIQ's Requirements (Limitations)
* **Fails Verifiable Grounding (FR2, FR3, RAI2):** A standalone model without access to an audited historical ticket store cannot retrieve real past incidents or cite verifiable source Ticket IDs.
* **Fails Safe Abstention (FR4, RAI2):** Without an explicit relevance threshold and abstention control, a simple pipeline may return a best-guess output even when an incoming ticket represents a novel or unsupported issue, rather than explicitly indicating that no sufficiently similar historical case was found.
* **Fails Privacy & Scope Boundaries (FR5, RAI1):** Passing raw user text directly to an AI capability without an input guardrail increases the risk of indexing or exposing Personal Identifiable Information (PII) and processing empty or out-of-domain inputs.
* **Fails Independent Maintainability (NFR4):** Coupling historical knowledge inside model weights prevents support teams from adding newly resolved tickets toward the < 5 minute update acceptance target without retraining the model.

### 4. Retrieval Evaluation and Data Leakage Prevention
* To prevent data leakage, the dataset will be separated into reference, validation, and test partitions after duplicate and near-duplicate removal.
- **Reference Set:** Used as the searchable historical ticket database.
- **Validation Set:** Used to evaluate retrieval behaviour and determine the similarity threshold.
- **Test Set:** Used only for final retrieval evaluation.
* Only the Reference Set will be indexed for retrieval. Validation and test tickets will not be included in the searchable database.
* The similarity threshold will be selected using validation results and kept unchanged during final testing.

---

## Step C2 - Identifying Architecture Needs from Requirements

Each additional component in the TicketIQ V1 conceptual architecture is justified by one or more requirements from `docs/week2_requirements.md` and evaluation criteria from `docs/week2_evaluation_criteria.md`:

| Requirement ID | What Does the Requirement Need? | Architecture Response (Component Added to V1) |
| :--- | :--- | :--- |
| **FR5, RAI1** | Incoming ticket text must be validated for domain scope (non-empty textual support queries) and redacted for configured PII patterns (names, emails, phone numbers, IPs) before model inference or indexing. | **Input Scope & Privacy Control** |
| **FR1, NFR1, RAI3** | The system must predict a primary ticket category and confidence score across imbalanced classes using only submission-time fields. Performance will be evaluated against the Macro-F1 >= 0.70 acceptance target. | **Ticket Classification Capability** |
| **FR2, NFR2, NFR4** | The system must search historical incidents and support adding new resolved tickets (targeting < 5 minutes update time) without retraining the classifier. | **Similarity Retrieval Capability** connected to an external **Historical Ticket Knowledge Source** |
| **FR3, FR4, RAI2** | Recorded resolutions must only be displayed when match similarity meets the usefulness threshold, always accompanied by a source Ticket ID; otherwise, the system must abstain. | **Relevance & Abstention Control** |
| **NFR1, NFR2, NFR3, RAI1, RAI2, RAI3** | The system must record classification predictions, confidence scores, retrieval scores, abstention decisions, source IDs, and end-to-end latency for systematic evaluation against the p90 < 2,000 ms acceptance target. Telemetry must avoid storing raw ticket text or unredacted PII unless explicitly necessary and appropriately protected. | **Evaluation & Telemetry Point** |
| **RAI4** | Historical data must be deduplicated, redacted for configured PII patterns, audited for resolution quality, and separated from post-submission leakage fields prior to indexing. | **Offline Data Audit & Sanitization Pipeline** (feeding the Historical Ticket Knowledge Source) |

---

## Step C3 - V1 Conceptual Architecture Overview

*(Refer to `docs/week2_architecture_v1.png` for the visual diagram)*

To adhere to V1 conceptual design principles, components are defined by their functional capabilities rather than premature technology commitments:

1. **User:** IT Help-Desk Agent submitting an incoming ticket (Subject + Initial Description).
2. **Application Interface (TicketIQ Triage Interface):** Captures ticket input and renders structured decision-support outputs (Predicted Category, Top-3 Similar Cases, Recorded Resolution with Source Ticket ID, or an Explicit Abstention Notice).
3. **Input Scope & Privacy Control:** Validates that the query is non-empty support text (`FR5`) and redacts configured PII patterns (`RAI1`) before forwarding sanitised text to downstream AI capabilities.
4. **Ticket Classification Capability:** Generates the primary category prediction and confidence score (`FR1`, `NFR1`, `RAI3`).
5. **Similarity Retrieval Capability:** Queries the knowledge source to rank and return the top-3 most similar historical ticket records (`FR2`, `NFR2`).
6. **Offline Data Audit & Sanitization Pipeline:** Processes the candidate historical dataset before indexing by checking data quality, removing duplicates, redacting configured PII patterns, assessing resolution quality, and excluding post-submission leakage fields (`RAI4`).
7. **Historical Ticket Knowledge Source:** Stores historical tickets that have passed the configured data-audit and sanitization pipeline, including available ticket identifiers, initial descriptions, categories, and resolutions that pass the data-quality checks (`NFR4`, `RAI1`, `RAI4`).
8. **Relevance & Abstention Control:** Evaluates whether retrieved candidates meet the defined similarity threshold. Passes usable recorded resolutions with Source IDs (`FR3`, `RAI2`) or triggers an explicit abstention alert for manual triage (`FR4`, `RAI2`). The similarity threshold is a retrieval filter, not proof that a historical resolution is correct or applicable. Retrieved resolutions remain historical references and require human verification.
9. **Evaluation & Telemetry Point:** Records classification predictions, confidence scores, retrieval scores, source Ticket IDs, abstention decisions, and end-to-end latency for offline evaluation against acceptance targets (`NFR1`, `NFR2`, `NFR3`). Telemetry must avoid storing raw ticket text or unredacted PII unless explicitly necessary and appropriately protected (`RAI1`). Index-update time and external AI/API costs will be measured separately against `NFR4` and `NFR5`.

---

## Step C4 - Architecture Decision Record (ADR) and Traceability

### 1. Architecture Decision Record (ADR)

| Decision | Requirement / Constraint | Alternatives Considered | Selected Option | Trade-off Accepted |
| :--- | :--- | :--- | :--- | :--- |
| **ADR 1: Evidence-Grounded Retrieval with Abstention Gate vs. Generative Troubleshooting** | **FR3, FR4, RAI2, NFR5** (No fabricated fixes, 100% source ID citation, >= 90% abstention target on unmatchable queries, US$0.00 external AI/API cost) | 1. Generative Language Model synthesizing custom fixes from prompt context.<br>2. Retrieval-only display without threshold filtering.<br>3. Retrieval capability paired with an explicit **Relevance & Abstention Control**. | **Option 3:** Retrieve verbatim historical resolutions gated by an explicit **Relevance & Abstention Control**. | Responses are limited to existing historical resolution text rather than tailored conversational prose, and borderline valid matches may be suppressed (false abstentions). This avoids free-form generative hallucination in the resolution display, but does not eliminate the risk of incorrect, outdated, or irrelevant historical resolutions, which still require human verification. |
| **ADR 2: Decoupled Classification Capability and Similarity Retrieval Capability** | **FR1, FR2, NFR1, NFR4, RAI3** (Acceptance targets: Macro-F1 >= 0.70 across imbalanced classes; index updates in < 5 min without classifier retraining) | 1. Single nearest-neighbour retrieval engine doing both case lookup and majority-vote classification.<br>2. Single classification model without historical case lookup.<br>3. Decoupled **Ticket Classification Capability** and **Similarity Retrieval Capability**, with execution order determined by implementation needs. | **Option 3:** Separate **Ticket Classification Capability** and **Similarity Retrieval Capability**, with execution order determined by implementation needs. | Increases pipeline maintenance overhead (two distinct capability modules to manage), but allows the classifier to optimise global decision boundaries for minority classes (`RAI3`), supports optional category-filtered retrieval if needed later, and enables training-free updates to the **Historical Ticket Knowledge Source** toward the < 5 minute acceptance target (`NFR4`). |
| **ADR 3: Dedicated Input Scope & Privacy Control Layer** | **FR5, RAI1** (Acceptance target: 0 exposed raw PII tokens on configured test patterns; immediate rejection of empty or invalid inputs) | 1. Relying solely on raw dataset pre-cleaning without runtime input filtering.<br>2. Sending raw queries directly to AI capabilities and masking outputs post-hoc.<br>3. Dedicated pre-inference **Input Scope & Privacy Control**. | **Option 3:** Dedicated **Input Scope & Privacy Control** placed before classification and retrieval capabilities. | Adds preprocessing overhead and risks over-redacting technical terms that resemble PII patterns. The control is designed to minimise PII exposure by validating and redacting inputs before downstream processing. Automated tests will assess whether configured PII patterns remain exposed. |
| **ADR 4: Local-First Target Architecture vs. Cloud Experimentation Environment** | **NFR3, NFR5, RAI1, Important Constraints** (Acceptance targets: p90 latency < 2,000 ms; US$0.00 external AI/API cost; student compute budget and privacy constraints) | 1. Cloud-hosted commercial LLM and managed vector database APIs.<br>2. Local-first execution with a local **Historical Ticket Knowledge Source** as the target architecture (using Google Colab only as an experimentation environment if needed). | **Option 2:** Local-first target execution with a local **Historical Ticket Knowledge Source**, while restricting Google Colab to experimentation on public/sanitised data. | Local-first execution limits maximum corpus scalability compared with distributed cloud infrastructure and still uses local hardware and compute resources. It avoids external AI/API network hops and supports the p90 < 2,000 ms latency target (`NFR3`), although actual performance must be verified through benchmarking on the target hardware. It also avoids sending ticket queries to third-party cloud providers when run locally (`RAI1`) and supports the US$0.00 external AI/API cost target (`NFR5`). If Google Colab is used for experimentation, code and data are processed in Google's cloud environment; therefore, only public or appropriately sanitised datasets should be used. |

---

### 2. Initial Requirements Traceability Matrix

| Objective | Requirement | Evaluation Criterion (with Acceptance Targets) | Architecture Element | Later Evidence (Week 3 - Week 14) |
| :--- | :--- | :--- | :--- | :--- |
| **O1** | **FR1, NFR1, RAI3, RAI4** | **Ticket Category Classification Accuracy** (Targets: Macro-F1 >= 0.70; Per-class Recall >= 0.55; 0% leakage) | **Ticket Classification Capability** & **Evaluation Point** | Held-out test split classification report, per-class confusion matrix, and leakage audit log (Weeks 5, 8, and 10). |
| **O2** | **FR2, NFR2, NFR4** | **Similar-Ticket Retrieval Relevance** (Targets: Hit Rate@3 >= 80%; Precision@3 >= 0.65; Index update < 5 min) | **Similarity Retrieval Capability** & **Historical Ticket Knowledge Source** | 50-query benchmark rubric evaluation sheet and timed 100-ticket index update log (Weeks 6, 9, and 10). |
| **O2, O3** | **FR3, FR4, RAI2** | **Evidence Grounding and Low-Relevance Abstention** (Targets: 100% Source ID presence; >= 90% abstention rate on unmatchable queries) | **Relevance & Abstention Control** & **TicketIQ Triage Interface** | Abstention test suite results across 30 matchable and 20 unmatchable/out-of-scope queries (Weeks 9 and 10). |
| **O1, O2** | **FR5, RAI1** | **PII Redaction Compliance & Input Validation** (TicketIQ will implement pattern-based PII detection and redaction for defined information types, such as email addresses, phone numbers and IP addresses. The system will not claim guaranteed detection of all personal information, particularly personal names that may require more advanced named-entity recognition techniques. Privacy testing will focus on predefined PII patterns and controlled test cases. Any limitations in detection coverage will be documented.) | **Input Scope & Privacy Control** & **Offline Data Sanitization Pipeline** | Automated privacy & boundary unit test logs on 50 seeded PII queries and 100 indexed records (Weeks 4 and 11). |
| **O1, O2, O3** | **NFR3, NFR5** | **Triage Response Latency and Cost Efficiency** (Targets: p90 latency < 2.0 s; External AI/API cost = US$0.00) | **End-to-End V1 Pipeline** monitored via **Evaluation Point** | Latency distribution benchmark report across 100 sequential queries and external AI/API cost log (Weeks 10 and 12). |

---

### 3. Final V1 Architecture Review Checklist

* **Does each major component support a requirement or evaluation need?**  
  Yes. Every box in the V1 architecture maps directly to at least one functional, non-functional, or Responsible AI requirement in the traceability matrix above.
* **Is any important data source, safety control, or evaluation point missing?**  
  No. The **Historical Ticket Knowledge Source** supplies domain grounding from audited records, **Input Scope & Privacy Control** and **Relevance & Abstention Control** enforce entry and exit boundaries, and the **Evaluation Point** captures performance telemetry against acceptance targets.
* **Have I added any technology or component that is not yet justified?**  
  No. All components are specified at the functional capability level, and optional features such as automated priority prediction have been excluded from V1 pending data validation.
* **Is there a simpler architecture that could still satisfy the requirements?**  
  No simpler architecture has yet been identified that satisfies all V1 requirements while retaining the proposed separation of responsibilities. The input privacy control and relevance/abstention control address distinct safety requirements, while a separately maintainable historical ticket store supports updates without classifier retraining. The design will be revisited after dataset auditing and baseline implementation.

---

## Part C Reflection

**Question:** *Which architecture decision involved the most important trade-off? Which requirement drove the decision, and what trade-off did you accept?*

**Reflection:**  
The architecture decision involving the most critical trade-off is **ADR 1: Evidence-Grounded Retrieval with an Explicit Relevance & Abstention Control versus Generative Troubleshooting**, which was directly driven by **FR3, FR4, and RAI2 (Transparency, Grounding, and Safe Abstention)**. In many modern AI help-desk tools, a generative model synthesizes a fluent, step-by-step troubleshooting guide even when retrieval confidence is mediocre. However, because TicketIQ relies on public ITSM datasets where historical resolutions may be uneven in quality and where an incorrect fix could disrupt IT operations, allowing free-form text generation introduces a severe risk of fabricated instructions. By choosing to display only verbatim recorded resolutions that pass data-quality checks and are gated behind a strict **Relevance & Abstention Control**, I accepted two key trade-offs: first, outputs are less conversational and borderline threshold settings may cause false abstentions; second, while this avoids free-form generative hallucination in the resolution display, the similarity threshold acts only as a retrieval filter rather than proof that a historical resolution is correct or applicable. Consequently, the architecture treats retrieved resolutions strictly as inspectable historical references rather than automated instructions, requiring human agent verification before action is taken.
