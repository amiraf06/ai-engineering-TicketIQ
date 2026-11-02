# TicketIQ: AI-Assisted Support Ticket Triage and Similar-Case Retrieval

TicketIQ is a proposed AI Engineering prototype for IT support teams. It will classify the text of a new support ticket, retrieve similar historical tickets, and display recorded resolutions only when the data provides a sufficiently relevant reference. It is a human decision-support tool, not an autonomous system.

## Problem Statement

Support staff may need to manually read incoming tickets, assign categories, and search historical tickets for related cases. Research and existing tools demonstrate that ticket classification and AI-assisted support are practical tasks to investigate [1–3]. This project has not independently measured the size of the problem in a specific organisation, so it will evaluate a prototype using public data rather than claim a measured business impact.

## Evidence of the Problem

- A 2021 help-desk study reported that using ticket comments and descriptions improved classification accuracy from 53.8% to 81.4% in its experiment [1]. This result is not a performance claim for TicketIQ.
- A Microsoft/Endava proof-of-concept describes automatic classification of support tickets and around 50,000 labelled tickets from its help-desk source [2].
- Atlassian documents AI suggestions based on work-item context and similar past work items [3]. Similar features already exist, so TicketIQ will not claim to be the first.

## Initial Related Work

| Work / solution | Existing capability | Relevant limitation or project distinction |
|---|---|---|
| Al-Hawari & Barham (2021) [1] | Machine-learning ticket classification in a help-desk system. | TicketIQ will separately evaluate whether historical-ticket retrieval and recorded resolution references are useful. |
| Microsoft / Endava ticket-classification proof-of-concept [2] | Text preprocessing, ticket-field classification, and a web-service example. | Its documented focus is classification; TicketIQ's project evaluation also covers retrieval relevance and evidence display. |
| Atlassian Jira Service Management AI suggestions [3] | Suggestions based on work-item context and similar past items. | TicketIQ will display the retrieved historical records as inspectable evidence. This is a design difference, not a claim of superiority. |
| ServiceNow priority lookup rules [6] | Priority can be determined by configured impact and urgency rules. | Priority prediction is optional because learning rule-generated labels may not provide meaningful added value. |

## Engineering Gap / Limitation

TicketIQ does not claim that similar systems do not exist. Its practical goal is to implement and evaluate a small public-data prototype that combines ticket-category prediction, similar-ticket retrieval, and visible references to usable historical resolutions. If the selected dataset's resolution field is unreliable, resolution suggestion will be excluded rather than fabricated.

## Proposed V1 Architecture

TicketIQ follows a modular, evidence-grounded architecture consisting of the following main components:

1. **Input Scope and Privacy Control** – Validates incoming support ticket text and applies configured PII redaction before processing.
2. **Ticket Classification Capability** – Predicts the primary category of the incoming support ticket.
3. **Similarity Retrieval Capability** – Searches the historical ticket knowledge source and retrieves the top three similar cases.
4. **Historical Ticket Knowledge Source** – Stores audited historical tickets, including available ticket identifiers, descriptions, categories and reliable recorded resolutions.
5. **Relevance and Abstention Control** – Determines whether retrieved cases meet the defined relevance threshold. If sufficient evidence is unavailable, the system abstains from displaying a resolution.
6. **Evaluation and Telemetry** – Records relevant system outputs and performance information for evaluation without unnecessarily storing raw ticket text or unredacted PII.

The classification and retrieval capabilities are designed as separate modules to support independent evaluation and improvement. Retrieved resolutions are presented as historical references for human verification, not as automatically generated or guaranteed solutions.

The proposed architecture is conceptual and may be refined after dataset selection, data auditing and baseline experiments.

## Initial Project Objectives

1. Develop and evaluate a baseline machine-learning model for classifying support-ticket text.
2. Build similar-ticket retrieval and show any reliable recorded resolution associated with matching cases.
3. Evaluate classification quality, retrieval relevance, and whether the system correctly abstains when no suitable historical case is found.

Priority prediction is an optional extension only if the labels are reliable and the evaluation avoids data leakage.

## Target Users

- IT help-desk agents.
- IT support teams who triage incoming tickets.

The system will support human decisions. It will not automatically close tickets or execute fixes.

## Proposed Data Sources

1. **Kaggle Customer Support Ticket Dataset** — https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset  
   The uploader describes over 8,000 tickets with subject, description, ticket type, priority, and resolution fields [4]. Its authenticity as organisational ITSM data is not established in the inspected description, and a public comment questions the usefulness of the resolution field. Audit the CSV and license before use; remove personal fields such as names and emails. Use recorded resolutions only if their quality is acceptable. Dataset selection is currently pending. Candidate datasets will be evaluated based on domain relevance, text availability, category labels, historical resolution quality, licensing and suitability for retrieval evaluation.Engineering Gap / Limitation
2. **Microsoft / Endava ITSM ticket-classification project** — https://github.com/pourabkarchaudhuri/itsm-ticket-classification  
   The repository describes an anonymised, labelled support-ticket dataset and classification proof-of-concept [2]. Verify current dataset availability and terms of use; the project description does not confirm reliable resolution text.
3. **UCI Incident Management Process Enriched Event Log** — https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log  
   UCI reports 24,918 incidents and 141,712 events under CC BY 4.0, but explicitly says textual-information attributes are not included [5]. It is not suitable for TicketIQ's primary text-classification or retrieval task.

## Project Status: Planning and Architecture Design

## Responsible AI Risks

- **Privacy:** remove personal fields before modelling and never expose them in retrieved records.
- **Wrong resolution:** present historical resolutions as references, show the source ticket, keep a human in the loop, and abstain when similarity is too low.
- **Missed critical categories:** report per-class metrics or macro-F1 and do not automatically downgrade serious tickets.
- **Data leakage:** exclude post-resolution information from initial-ticket prediction, remove duplicates before data splitting, and check any priority model against rule-generated labels [6].

## References

[1] Al-Hawari, F. & Barham, H. (2021). “A machine learning based help desk system for IT service management.” https://doi.org/10.1016/j.jksuci.2019.04.001

[2] Microsoft / Endava, “ITSM ticket classification” proof-of-concept. https://github.com/pourabkarchaudhuri/itsm-ticket-classification

[3] Atlassian Support, “About suggestions on work items.” https://support.atlassian.com/jira-service-management-cloud/docs/about-suggestions-on-issue-view/

[4] Suraj, “Customer Support Ticket Dataset,” Kaggle. https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset

[5] UCI Machine Learning Repository, “Incident management process enriched event log.” https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log

[6] ServiceNow, “Define priority lookup rules.” https://www.servicenow.com/docs/r/it-service-management/incident-management/def-prio-lookup-rules.html

## Weekly Progress

This is an initial project roadmap and may change after the dataset audit and proposal feedback. Planned work is not marked as completed in advance.

| Week | Planned work | Expected output | Status |
|---|---|---|---|
| W1 | Define the problem, review initial evidence and existing solutions, and identify possible public datasets. | Project scope draft and initial README. | Draft prepared; dataset audit pending |
| W2 | Finalise the project boundaries, main requirements, evaluation plan, and high-level design. | Requirements, evaluation criteria, and V1 architecture. | Completed |
| W3 | Download and inspect candidate datasets; set up a repeatable process to load and prepare the chosen data. | Dataset notes and initial data-preparation workflow. | Planned |
| W4 | Check data quality, labels, duplicates, missing values, privacy concerns, and possible data leakage. | Data audit and cleaning decisions. | Planned |
| W5 | Choose practical baseline methods for classifying ticket text and finding similar cases. | Model-choice rationale and baseline experiment plan. | Planned |
| W6 | Build an early end-to-end prototype using the prepared data and selected baseline methods. | First working pipeline or prototype. | Planned |
| W7 | Present the proposal and refine the project based on feedback. | Proposal slides and updated scope. | Planned |
| W8 | Semester break; keep the workload light and organise notes or backlog if needed. | Updated task list, if needed. | Semester break |
| W9 | Improve similar-ticket search and connect retrieved cases to their recorded resolution where the data supports it. | Retrieval workflow with visible source cases. | Planned |
| W10 | Test the system on held-out data and inspect incorrect classifications and irrelevant matches. | Evaluation results and error analysis. | Planned |
| W11 | Add repeatable tests for data processing and core application behaviour; automate suitable checks where feasible. | Basic test suite and quality checks. | Planned |
| W12 | Package the prototype so another person can run or access it in the intended project environment. | Demonstrable deployed or locally runnable prototype. | Planned |
| W13 | Add basic error logging and record cases where predictions or retrieval perform poorly. | Logs and a short improvement plan. | Planned |
| W14 | Review privacy, human oversight, unsupported suggestions, and other Responsible AI risks; apply practical safeguards. | Responsible AI review and documented mitigations. | Planned |
| W15 | Demonstrate TicketIQ, explain the approach and evaluation results, and be clear about limitations and future work. | Final showcase and project summary. | Planned |
