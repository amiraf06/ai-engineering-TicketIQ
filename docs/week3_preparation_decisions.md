# Week 3: Data Preparation Decisions

## 1. Purpose

This document records the preparation methods considered, selected decisions, and trade-offs for the TicketIQ dataset.

The objective is to prepare a reproducible dataset for the later ticket classification pipeline while preserving data integrity and documenting unresolved quality and privacy risks.

## 2. Selected Input Features and Target

The preparation process retains only:

- `Ticket Subject` — input feature
- `Ticket Description` — input feature
- `Ticket Type` — provisional classification target

Other columns are excluded from the prepared dataset.

Customer identifiers and personal information fields are excluded. Post-submission information, such as resolution details, response time, resolution time, and customer satisfaction, is also excluded to reduce potential data leakage.

`Ticket Priority` is not used as a target in the current project scope.

## 3. Preparation Decisions and Alternatives

| Area | Alternatives Considered | Selected Decision | Reason and Trade-off |
|---|---|---|---|
| Missing values | Remove incomplete records, impute missing values, or reject the dataset | Fail if selected fields contain missing values | No missing values were found in the three selected columns. Failing fast avoids introducing unsupported replacement values. |
| Text formatting | Keep original text or normalize whitespace | Trim leading and trailing whitespace | A minimal transformation improves consistency while preserving the original wording. |
| Email addresses | Retain, remove entire records, or redact detected email patterns | Redact obvious email patterns | Reduces exposure of direct contact information while retaining the surrounding ticket text. Pattern-based redaction may not detect every format. |
| Phone-like values | Automatically redact or flag for review | Flag potential phone-number patterns without automatic redaction | Some numeric patterns may represent order numbers, dates, or other legitimate ticket details. Manual review is required before external publication. |
| Duplicate records | Delete all duplicates or retain them for further analysis | Audit and retain records during this preparation stage | Automatic deletion could remove useful evidence or conceal repeated-label conflicts. Duplicate handling must be addressed before model evaluation to prevent train-test leakage. |
| Conflicting labels | Automatically assign a majority label, delete records, or retain for investigation | Retain conflicting records and document the issue | There is insufficient evidence to determine the correct label automatically. Arbitrary reassignment could introduce incorrect ground truth. |

## 4. Data Quality Findings

The source dataset contains 8,469 data records and 17 columns.

The prepared dataset contains:

- 8,469 records
- 3 selected columns
- 0 missing values in the selected columns
- 5 validated `Ticket Type` categories

The preparation audit identified:

- 42 duplicate rows based on the selected subject, description, and label columns. These records were retained.
- 49 description-level groups with conflicting `Ticket Type` labels, affecting 446 records.
- 85 subject-description groups with conflicting labels, affecting 205 records.

These findings indicate potential label-quality and duplicate-related risks. They do not establish that every affected record is incorrectly labelled.

## 5. Privacy and Data Handling

Obvious email patterns were redacted from the selected text fields.

Potential phone-number patterns were flagged but not redacted. Other unrecognized personal information may remain in the ticket descriptions.

Therefore, the prepared dataset must remain local until a further privacy review is completed. The current preparation process does not guarantee complete anonymisation.

The raw and processed CSV files are excluded from Git tracking through `.gitignore`.

## 6. Validation and Traceability

After preparation, the output CSV was reloaded and checked.

The validation confirmed:

- Expected output columns are present.
- Output row count matches the source row count.
- No missing values remain in the selected fields.
- All target labels belong to the expected five-category label set.

SHA-256 hashes of the source and prepared output were recorded in `data/week3_manifest.json` to support file integrity checks and traceability.

## 7. Limitations and Deferred Work

The dataset represents general customer support tickets and is not confirmed to be a dedicated IT service management (ITSM) dataset.

The following work remains necessary before model development:

1. Review potential personal information, including flagged phone-like patterns.
2. Investigate conflicting labels and establish a documented label-quality policy.
3. Handle duplicate and repeated input records before train-test splitting to reduce data leakage risk.
4. Reassess whether the dataset is sufficiently suitable for the intended IT ticket classification use case.

No model training or performance evaluation is performed in this preparation stage.

## 8. Final Decision

The selected preparation approach prioritises data integrity, minimal text transformation, privacy awareness, and traceability.

Records with unresolved duplicate or label-quality concerns are retained for investigation rather than being automatically removed or relabelled.

The resulting dataset is a prepared intermediate artefact, not yet a fully validated model-ready dataset.