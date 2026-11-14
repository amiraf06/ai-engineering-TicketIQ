# Week 3 — Data Preparation Decisions

## Selected pathway
Pathway B (CSV/Excel) is selected. Raw source: `data/raw/customer_support_tickets.csv`. Prepared output: `data/processed/prepared_table.csv`. Manifest: `data/week3_manifest.json`. Notebook: `notebooks/week3_pipeline.ipynb`, executed in Google Colab. Raw source remains unchanged.

## Selected fields
- Inputs: `Ticket Subject`, `Ticket Description`
- Provisional target: `Ticket Type`
- Exclude all other source fields, including direct identifiers, priority and post-submission/outcome fields.

## Alternatives compared
| Area | Approach A | Approach B (selected if all labels remain) |
|---|---|---|
| Whitespace | Trim outer whitespace | Same |
| Email patterns | Redact detected emails | Same |
| Conflicting normalised input groups | Retain and flag | Exclude complete groups with multiple labels |
| Exact duplicate modelling rows | Retain | Remove after conflict exclusion |
| Phone-like patterns | Flag only | Flag only |
| Brace placeholders | Preserve | Preserve |

Approach B prevents identical normalised inputs carrying contradictory labels and reduces duplicate leakage. Exclusion does not prove which source label is correct. The notebook compares actual row counts, duplicate counts, missingness and class counts; it stops if any of the five expected labels disappear.

## Validation and lineage
Reload the prepared CSV and verify schema, row count, missingness, all five labels, exact duplicates, conflicting normalised inputs, non-empty output and file size. The B4 manifest records source/output paths and SHA-256 hashes, processing method, source metadata, comparison counts and limitations. Reopen the manifest and recompute both hashes.

## Privacy and storage
Exclude `Customer Name` and `Customer Email`; redact detected emails; flag phone-like patterns without automatic redaction. Pattern checks cannot guarantee anonymisation. Keep raw/prepared CSV private, outside public Git. Colab `/content` is temporary; persist outputs in an access-controlled location.

## Limitations and required decision
1. General customer support, not verified ITSM incident data.
2. `Ticket Type` is uploader-supplied, not independently verified ground truth.
3. Excluded conflict groups remain in unchanged raw source.
4. Phone-like patterns and other PII may remain.
5. All descriptions contain a brace-delimited placeholder pattern.

**Dataset suitability decision:** formally broaden TicketIQ to general support-ticket classification (and revise Week 1/2 framing), or replace this source with suitable ITSM data before claiming real IT help-desk applicability.

Part B is complete only after the Colab notebook executes successfully, the two approaches are compared with actual evidence, B3 passes, and B4 hashes are verified.
