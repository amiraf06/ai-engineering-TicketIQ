# Week 3 — Data Inventory

## Source
- Dataset: Customer Support Ticket Dataset
- URL: https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset
- File: `customer_support_tickets.csv`
- Format: structured CSV
- Observed source dimensions: 8,469 records × 17 columns
- Version 1; author `suraj520`; CC0 1.0 Universal as displayed on Kaggle (recheck before redistribution).

The dataset represents general customer support. Its public description does not establish that records are authentic ITSM incidents. It is a provisional proxy, not evidence of real IT help-desk applicability.

## Requirement-to-data mapping (A1)

| Requirement | Data needed | Fields / evidence | Constraint |
|---|---|---|---|
| FR1 | Initial ticket text | `Ticket Subject`, `Ticket Description` | General support, not verified ITSM. |
| FR2 | Text for TF-IDF | Same text fields | Template-heavy content; fit vectorizer on training data only. |
| FR3/FR4 | Shared target | `Ticket Type` | Five supplied labels; quality provisional. |
| RAI1 | Exclude identifiers | Exclude name/email columns; redact detected emails | Phone-like values flagged; residual PII possible. |
| RAI2 | Initial-submission information | Subject/description only; exclude resolution/status/response/outcome fields | No post-submission inputs. |
| RAI4 | Duplicate/conflict checks | Subject, description, target | Initial audit: 42 duplicate rows in selected projection; 85 conflicting combined input groups involving 205 records. |
| NFR3 | Repeatable preparation | Explicit path, hashes, manifest | Model seed/configuration recorded later. |

## Inventory and A3 evidence

| Source ID | Filename / URL | Type and purpose | Version/date/owner | Access/rights | Inspection evidence |
|---|---|---|---|---|---|
| S01 | `customer_support_tickets.csv` — Kaggle URL above | CSV for candidate support-ticket classification | Version 1; `suraj520`; metadata showed 3.95 MB and ~3 years since update at inspection | Public Kaggle; CC0 1.0 displayed; recheck before redistribution | `notebooks/week3_pipeline.ipynb`: schema, dtypes, missingness, duplicates, labels, text and consistency audits |
| S01-SUBSET-01 | First five records | Representative subset | Derived from S01 | Same rights; keep private | Notebook table shows subject, target and text lengths |
| S01-SUBSET-02 | One row per `Ticket Type` | Label-stratified subset | Derived from S01 | Same rights; keep private | Notebook table shows categories and text lengths |

## Selected fields
Inputs: `Ticket Subject`, `Ticket Description`. Provisional target: `Ticket Type`. All other 14 fields are excluded, including direct identifiers, priority and post-submission/outcome fields.

## Initial findings
- 8,469 records; 17 columns.
- No missing values in selected subject, description and target fields.
- 0 full-row duplicates; 0 duplicate Ticket IDs.
- 42 duplicate rows in the selected three-column projection.
- 16 unique subjects; all occur with all five labels.
- All 8,469 descriptions contain a brace-delimited placeholder pattern.
- 49 normalised description groups have multiple labels (446 records).
- 85 normalised subject-description groups have multiple labels (205 records).
- Initial pattern scan: 80 email patterns in descriptions; 102 phone-like patterns flagged. Pattern counts are not counts of confirmed individuals or phone numbers.

## Storage and privacy
Raw source: private Colab `data/raw/`. Prepared output: `data/processed/prepared_table.csv`. Manifest: `data/week3_manifest.json`. `/content` is temporary; persist outputs to a private access-controlled location. Do not commit CSVs to public GitHub. Prepared data is not guaranteed fully anonymised.

## Suitability limitation
The source is general customer support, not verified ITSM incident data. Only one of five categories is `Technical issue`. Either broaden the project domain formally to general support-ticket classification or replace the source with an appropriate ITSM dataset before claiming real IT help-desk applicability.
