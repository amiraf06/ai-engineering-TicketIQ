---
title: "TicketIQ — Week 4 Data Quality & Bias Report"
author: "Amir Asyraaf | AI Engineering, UTM"
date: "18 November 2026"
---

<style>
body{font-family:"DejaVu Sans",Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#1a1a1a;}
h1,h2{color:#15314d;border-bottom:1px solid #d7dde3;padding-bottom:3px;}
table{border-collapse:collapse;width:100%;table-layout:fixed;margin:6px 0 12px 0;font-size:8pt;}
th,td{border:1px solid #c7ccd1;padding:3px 5px;line-height:1.25;vertical-align:top;text-align:left;word-wrap:break-word;overflow-wrap:break-word;}
th{background:#eef2f6;}
code{background:#f2f2f2;padding:0 3px;border-radius:3px;font-size:91%;}
td code,th code{word-break:break-all;}
p,li{margin:4px 0;}
h2{margin-top:16px;margin-bottom:6px;}
</style>

**Repository:** github.com/amiraf06/ai-engineering-TicketIQ
**Audit scope:** Topic 3 Part B/C tabular pathway (Pathway B — CSV/Excel)

## 1. Project and Data Overview

TicketIQ predicts a support ticket's category (`Ticket Type`) from its `Ticket Subject` and `Ticket Description`, for review by IT help-desk agents (`README.md`; `docs/week2_requirements.md`).

Two Week 2 requirements anchor this audit:

- **RAI1 (Privacy)** — personal identifiers not required for classification shall be excluded from model inputs and public output examples.
- **RAI4 (Data Integrity)** — exact and near-duplicate records shall be checked before the dataset is split for training/testing.

**Topic 3 pathway audited:** B — CSV/Excel (tabular), covering both preparation stages:

| Stage | Documented path | Manifest | What is actually in the repository |
|---|---|---|---|
| Part B prepared artefact | `data/processed/prepared_table.csv` | `data/week3_manifest.json` | Differently-named, differently-shaped file instead — §2. |
| Part C V1 pipeline output | `data/pipeline_v1/tabular/prepared_table.csv` | `data/pipeline_v1/tabular/pipeline_manifest.json` | No CSV at that path or in Git history — §2. |

**Audit method:** instead of a 10–20 item manual sample, this audit re-ran the quantitative checks (hashing, row/column counts, duplicate and label-conflict detection, email/placeholder pattern scans) against the **full population** of both committed CSVs (8,469 rows each), cross-checked against all Week 2–3 docs and both manifests, plus a small qualitative read of raw rows for text-content checks. **Limitation:** this covers only what the public repository contains as of 18 Nov 2026 — the private Google-Drive copy of the true Approach-B `prepared_table.csv` could not be opened, so its validity rests on the self-reported manifest alone (marked N.V. below where relevant).

**Checkpoint A1:** if `Ticket Type` or either text field were missing or corrupted, FR1 (ticket intake) and FR3/FR4 (both classifiers) would fail outright, since O1–O3 all depend on these three columns.

## 2. Five-Dimension Quality Scorecard

<table>
<colgroup><col style="width:11%"><col style="width:28%"><col style="width:22%"><col style="width:27%"><col style="width:12%"></colgroup>
<tr><th>Dimension</th><th>Finding</th><th>Evidence</th><th>Impact</th><th>Decision</th></tr>
<tr><td>Completeness</td><td>The 3 modelling columns have 0 missing values across all 8,469 records.</td><td><code>isna().sum()</code> re-run on both committed CSVs.</td><td>FR1–FR4 are not blocked by missing values.</td><td><strong>Pass</strong></td></tr>
<tr><td>Consistency</td><td><code>ticketiq_dataset.csv</code> ≠ the output <code>week3_manifest.json</code> describes: different SHA-256; 8,469 rows, not 8,240; still has the 42 duplicates / 85 conflicting groups Approach B should remove.</td><td>Hash/row-count recheck (Appendix). A second script, <code>week3_data_preparation.py</code>, targets the same paths under different logic (retains duplicates, no auto-correction).</td><td>NFR3 (reproducibility) can't be confirmed from the repo alone.</td><td><strong>Review</strong></td></tr>
<tr><td>Accuracy</td><td>100% of descriptions still carry an unresolved placeholder (e.g. <code>{product_purchased}</code>); 100% of <code>Customer Email</code> values use only reserved <code>example.*</code> domains, never a real one.</td><td>Regex scan, raw CSV.</td><td>Text may be template-generated, not organic — deeper than the domain-mismatch already on file; O1 features may not transfer to real deployment.</td><td><strong>Review</strong></td></tr>
<tr><td>Timeliness</td><td>The source was ~3 years old at Topic 3 inspection; Week 2 sets no explicit freshness requirement.</td><td><code>week3_data_inventory.md</code> inspection note.</td><td>Ticket phrasing/products may have shifted; nothing currently checks this.</td><td><strong>Warning</strong></td></tr>
<tr><td>Uniqueness</td><td>42 duplicate rows + 85 conflicting label groups (205 records) confirmed in the committed file; Approach B is documented to cut these to 24 / 0, but that cleaned file isn't the one in the repo.</td><td><code>duplicated()</code> re-run vs. <code>week3_manifest.json</code>.</td><td>RAI4 is satisfied by design, not yet by the committed artefact.</td><td><strong>Design: Pass.<br>Artefact: Review</strong></td></tr>
</table>

## 3. Validation Findings

**V1 — traceable to RAI4.** *Condition:* no record used for modelling may share a normalised (Subject + Description) pair with more than one `Ticket Type`. *Tested:* full population, `data/processed/ticketiq_dataset.csv`. *Result:* **Fail** — 85 groups / 205 records still conflict, and 42 exact duplicates remain (matches the pre-exclusion figures in `docs/week3_data_inventory.md`). The manifest's self-reported zero-conflict, 8,240-row Approach-B table is **N.V.** here, since that file cannot be independently retrieved. *Action:* do not promote the current file to W5 modelling; re-export the true Approach-B table, or re-verify the private-Drive copy's hash against the manifest, before splitting data.

**V2 — traceable to RAI1.** *Condition:* no file in the public repository may expose a real personal identifier. *Tested:* full population, both committed CSVs. *Result:* **Mixed.** Description text passes (0/8,469 embedded emails remain post-redaction). The raw file **fails** on `Customer Name`/`Customer Email` being present and public for all 8,469 rows — though every email is a synthetic `example.*` placeholder, so no real mailbox is exposed; whether `Customer Name` is synthetic is **N.V.** *Action:* remove `data/raw/customer_support_tickets.csv` from the public repository and its Git history regardless of the apparent synthetic status, since this is exactly what the project's own notebook and `week3_preparation_decisions.md` already say not to do.

## 4. Duplicate, Anomaly and Coverage Findings

Duplicates/conflicts are summarised in Sections 2–3. Two coverage checks:

- **Label balance** (5 `Ticket Type` categories): Refund request 1,752, Technical issue 1,747, Cancellation request 1,695, Product inquiry 1,641, Billing inquiry 1,634 — each class is 19.3–20.7% of the data, i.e. reasonably balanced. RAI3 is therefore not a major concern for this V1 dataset.
- **Domain coverage**: only `Technical issue` (1,747 rows, 20.6%) is plausibly IT-specific; the other 79.4% are general retail/e-commerce categories. This quantifies, rather than removes, the domain-suitability limitation already recorded in `docs/week3_data_inventory.md`.

**Limits of this evidence:** coverage was measured on the raw/committed (pre-exclusion) file; the true Approach-B subset's class balance after removing 205 conflicting records was not independently recomputable (N.V.), though the manifest states all five labels survive.

## 5. Bias Assessment

**Plausible risk: pipeline-induced + representation bias from templated text and category composition.** Source/preparation decision: the Kaggle source appears template-generated and skews toward general retail support → data gap/skew: a classifier may learn placeholder/template structure rather than genuine free-text signal, with limited real examples of IT-specific phrasing → potential effect: weaker real-world performance on genuinely technical tickets than test-set metrics would suggest, undermining the stated help-desk use case → proposed control: strip or neutralise placeholder tokens before TF-IDF fitting, and report the `Technical issue` class's metrics separately rather than only macro-averaged, since it is the class closest to the stated deployment context. This is a plausible risk, not proven unfairness — no model has been trained yet.

## 6. Privacy, Rights and Governance

| Question | What this audit found |
|---|---|
| Provenance/version | S01, Kaggle, `suraj520`, "Version 1"; raw-file SHA-256 matches both manifests exactly — provenance is internally consistent. |
| Rights/permissions | CC0 1.0 "as displayed"; both manifests themselves still flag this as unverified ("recheck before redistribution") — **N.V.**, never completed. |
| Privacy/sensitive data | See V2: raw `Customer Name`/`Customer Email`/`Age`/`Gender` for all 8,469 rows is currently public, contradicting the project's own rule in `notebooks/week3_pipeline.ipynb` ("Do not commit raw/prepared CSV files to public GitHub") and `week3_preparation_decisions.md`. |
| Consent/collection basis | Not applicable — obtained via public Kaggle download; no direct data collection from subjects by this project. |
| Ongoing maintenance | Amir should review repository contents before every weekly commit; any change to the raw source, or any step that widens who can see the repository, should trigger re-review. |

**Required action:** purge `data/raw/customer_support_tickets.csv` from the public repository and its Git history (the repo currently has a single commit, `2a55aea`, so `git rm --cached` + `git commit --amend` + a force-push removes it cleanly); replace or remove `data/processed/ticketiq_dataset.csv` until it matches the manifest beside it.

## 7. Mitigation and Impact on Requirements

1. **Reconcile the repository's artefacts with RAI1/RAI4** — remove the raw CSV from history; commit a verifiable Approach-B `prepared_table.csv` or clearly document that it is intentionally private and how a reviewer can verify its hash. *Owner:* Amir. *When:* before the next commit, ahead of W5. *Residual risk:* if the repository has already been cloned, forked, or indexed while public, a history rewrite cannot retroactively un-expose those copies.
2. **Resolve the dataset-authenticity/domain question** — formally decide to (a) broaden project framing to general customer support, (b) source genuine ITSM data, or (c) keep this source but treat the template-placeholder finding as an accepted V1 limitation with a concrete plan to validate against real examples later. *Owner:* Amir. *When:* before W5 preprocessing choices are locked in. *Affects:* O1–O3, FR1–FR6, and the RAI block jointly.

## 8. Quality-Gate Decision

**Decision: GO WITH CONDITIONS**, scoped to the Topic 3 Part B/C tabular output (Subject + Description + Type) as the basis for W5/W6 modelling.

**Evidence:** (1) the documented preparation logic — trim, redact, exclude conflicting groups, de-duplicate — is sound and, where it actually ran in `notebooks/week3_pipeline.ipynb`, is hash-traceable against the raw source; (2) however, the repository's own committed artefacts do not yet let a third party independently re-verify that claim, and a raw file with structured (if apparently synthetic) personal fields is currently public in violation of the project's own stated rule.

**Conditions:** complete both mitigations in Section 7 before relying on this data for graded model results.

**Residual risk:** even after both fixes, whether this dataset's templated, majority-non-technical text meaningfully represents the real IT help-desk deployment context remains open.

**Re-review trigger:** reproducing the 8,240-row/zero-conflict figure once `prepared_table.csv` is verifiable from the repository; any change to the raw source file; or a decision to change the dataset itself.

---

## Appendix: Supporting Evidence *(not counted toward the 2–3 page target)*

**Hashes, for independent re-verification:**

- `data/raw/customer_support_tickets.csv` → `b06a9cde84da65db388bd964d75f88ee1eed96607cf75d0c35f09c3f11bf8bea` — **matches** the `source_sha256` recorded in both manifests.
- `data/processed/ticketiq_dataset.csv` → `5aaa5ecb6e21aab8fd08b840ad572ee86e12cc609970c55fff136fc18b7fa399` — **does not match** `data/week3_manifest.json`'s `prepared_sha256` (`45c80b20f6f492e7893576f55934d512bb102b1ae7b197b8ba593dc59289880e`).
- No file in the repository or its Git history matches `data/pipeline_v1/tabular/pipeline_manifest.json`'s `output_sha256` (`0b812b7c3d4cd126b66f06c703c30bafa06eedbca13b7ee3ce59c3a1d8b278ba`).

**Verification method:** `hashlib.sha256()` over each file; `pandas.DataFrame.duplicated()` on the 3 selected columns; a `groupby` on normalised (lower-cased, whitespace-collapsed) Subject+Description to count label-conflicting groups; `str.contains()` with the project's own email/placeholder regex patterns from `notebooks/week3_pipeline.ipynb`; `git log --all` to confirm the repository's single-commit history.

**Report status:** Week 4 individual audit, prepared for repository commit and e-learning submission.
