# TicketIQ: Week 3 Pipeline Decisions, Stage Contracts and Traceability

**Version:** 1.0  
**Status:** Week 3 V1 Data Pipeline Decisions

---

## 1. Purpose and Requirement Traceability

This document records the engineering decisions made when developing the TicketIQ V1 data preparation pipeline. The pipeline prepares support-ticket text and category labels for subsequent machine-learning experiments.

The selected pipeline supports the following Week 2 objectives and requirements:

| Requirement ID | Requirement / Objective | Pipeline Contribution |
|---|---|---|
| O1 | Develop a baseline model to classify support tickets. | Prepares consistent ticket text and category labels for baseline training. |
| O2 | Develop an advanced model for the same classification task. | Provides the same prepared dataset for advanced model development. |
| O3 | Compare both models using standard evaluation metrics. | Establishes a consistent prepared dataset before model splitting and evaluation. |
| FR1 | Accept ticket subject and initial description as text input. | Selects `Ticket Subject` and `Ticket Description`. |
| FR2 | Preprocess selected ticket text and transform it into numerical features using the agreed method. | Performs initial text cleaning and preparation. TF-IDF feature extraction is outside this Week 3 pipeline. |
| RAI1 | Exclude unnecessary personal identifiers from model inputs and public examples. | Excludes unrelated columns and redacts detected email addresses. |
| RAI2 | Use only information available at initial ticket submission. | Uses ticket subject, description and category label; excludes post-submission information. |
| RAI4 | Check exact and near-duplicate records before splitting. | Removes exact duplicate modelling rows and excludes conflicting normalized input groups before later splitting. |

The pipeline prepares data but does not train either classifier. Model training, TF-IDF fitting, train/test splitting and model evaluation remain subsequent activities.

## 2. Selected Data Source

**Dataset:** Customer Support Ticket Dataset  
**Platform:** Kaggle  
**Owner:** suraj520  
**Source file:** `customer_support_tickets.csv`  
**Source format:** CSV  
**Selected data type:** Tabular data

The dataset contains 8,469 data rows in the original CSV file, excluding the header row.

Three columns were selected for the modelling dataset:

- `Ticket Subject`
- `Ticket Description`
- `Ticket Type`

`Ticket Type` is retained as the target category label. The dataset contains five observed categories:

1. Billing inquiry
2. Cancellation request
3. Product inquiry
4. Refund request
5. Technical issue

The selected fields represent the ticket information and category label required for the intended classification task.

**Dataset suitability limitation:** The selected dataset is a general customer-support dataset. It has not been verified as an authentic IT service-management (ITSM) help-desk dataset. Its suitability for TicketIQ's intended IT-support context therefore requires further evaluation.

## 3. Part B Preparation Comparison and Evidence

Two preparation approaches were evaluated during Part B.

| Evidence | Approach A | Approach B |
|---|---:|---:|
| Initial records | 8,469 | 8,469 |
| Prepared records | 8,469 | 8,240 |
| Conflicting input groups excluded | Not applied | 85 |
| Records excluded due to conflicting groups | Not applied | 205 |
| Exact duplicate modelling rows removed | Not applied | 24 |
| Final modelling columns | Not established as the selected clean output | 3 |

Approach B was selected because it applies additional data-integrity checks before the dataset is used for machine-learning experiments.

The selected approach:

- Trims leading and trailing whitespace.
- Redacts detected email addresses.
- Identifies conflicting category labels associated with normalized ticket inputs.
- Excludes conflicting input groups.
- Removes exact duplicate modelling rows.

The resulting prepared dataset contains **8,240 rows and 3 columns**.

The recorded validation checks confirmed that the prepared output:

- Exists and is non-empty.
- Has the expected three-column schema.
- Contains 8,240 rows.
- Has no missing values in the selected modelling columns.
- Retains all five observed category labels.
- Contains no exact duplicate modelling rows.
- Contains no remaining conflicting normalized input groups.

These results support selecting Approach B for the V1 pipeline.

However, removing conflicting groups does not prove that every remaining category label is correct. The original labels are supplied by the dataset and have not been independently verified.

## 4. Selected Preparation Configuration

The selected tabular preparation configuration is:

| Setting | Selected Configuration |
|---|---|
| Data type | Tabular |
| Input format | CSV |
| Source file | `customer_support_tickets.csv` |
| Selected columns | `Ticket Subject`, `Ticket Description`, `Ticket Type` |
| Text cleaning | Trim leading and trailing whitespace |
| Email handling | Redact detected email addresses |
| Conflict handling | Exclude conflicting normalized input groups |
| Duplicate handling | Remove exact duplicate modelling rows |
| Expected prepared rows | 8,240 |
| Expected columns | 3 |
| Target label | `Ticket Type` |

The pipeline preserves the three selected modelling columns and does not perform tokenization, TF-IDF vectorization, feature extraction or model training at this stage.

## 5. Accepted Limitations and Engineering Trade-offs

The following limitations are accepted for the V1 pipeline:

1. **Dataset domain limitation:** The dataset represents general customer support rather than a verified ITSM environment.
2. **Label reliability:** The supplied `Ticket Type` labels are treated as available target labels but are not independently confirmed as ground truth.
3. **Residual privacy risk:** Detected email addresses are redacted, but phone-like patterns were flagged rather than redacted. Other residual personal information may remain.
4. **Conflict exclusion:** Excluding conflicting normalized input groups improves consistency but reduces the available training records.
5. **No semantic feature extraction:** TF-IDF and other numerical feature extraction are reserved for the later modelling pipeline.
6. **No production deployment:** This is an academic V1 data pipeline and does not establish production-level reliability or operational readiness.

These limitations will be considered during subsequent dataset suitability, data-quality and Responsible AI assessments.

## 6. ETL / ELT Decision

**Selected approach: ETL (Extract, Transform, Load).**

The pipeline follows an ETL-style workflow:

- **Extract:** Read the selected CSV source from the raw data directory.
- **Transform:** Inspect the dataset, select modelling columns, clean text, redact detected emails, exclude conflicting groups and remove exact duplicate modelling rows.
- **Load:** Save the prepared output as a CSV file in the pipeline output directory.

ETL is selected because the V1 workflow prepares and validates the dataset before storing the resulting modelling artefact.

The prepared output is intended to be consumed by subsequent machine-learning development rather than queried directly from the original raw dataset.

## 7. Batch / Streaming Decision

**Selected approach: Batch processing.**

The source is a static CSV dataset containing 8,469 records. The current project workflow processes the available records as a dataset rather than receiving continuous incoming ticket events.

Batch processing is suitable because:

- The source data is available as a complete file.
- Preparation and validation can be executed in a controlled run.
- The pipeline can be rerun to verify repeatability.
- The project does not currently require real-time ingestion or continuous processing.

Streaming is not selected because the current V1 scope does not include a live ticket-ingestion service or event-streaming infrastructure.

## 8. Output Storage and Provenance

The pipeline uses the following output locations:

**Part B prepared dataset:**

`data/processed/prepared_table.csv`

**Part B lineage manifest:**

`data/week3_manifest.json`

**Part C V1 pipeline output:**

`data/pipeline_v1/tabular/prepared_table.csv`

**Part C pipeline execution manifest:**

`data/pipeline_v1/tabular/pipeline_manifest.json`

The pipeline manifest records execution metadata, including:

- Pipeline version.
- Execution timestamp.
- Data type and configuration.
- Processing method.
- Source file path and SHA-256 fingerprint.
- Prepared output path and SHA-256 fingerprint.
- Source-to-output mapping.
- Inspection results.
- Output validation information.

The repeatability smoke check re-executes the selected pipeline and compares source fingerprints, output fingerprints and source-to-output mappings.

A successful repeatability check provides evidence that the pipeline produced matching outputs under the current execution environment. It does not establish complete cross-environment reproducibility or comprehensive data quality.

**Provenance and access caveat:** The source dataset's Kaggle page displayed CC0 1.0 Universal as its access-rights information. This should be rechecked before redistribution. Prepared data may also contain residual personal information, so only authorised and non-sensitive artefacts should be committed to the public repository.

## 9. Pipeline Stage Contracts and Failure Responses

| Stage | Contract / Expected Evidence | Failure Response |
|---|---|---|
| Ingest | The selected CSV source exists, is readable and is available at the configured path. | Stop execution if the source is missing, unreadable or invalid. Verify the file path and source integrity before rerunning. |
| Inspect | The source can be loaded and its structure, columns, dimensions, missing values and exact duplicates can be inspected. | Stop or flag the source if it is empty, unreadable or has an unexpected structure. Investigate the source before preparation. |
| Prepare / Transform | The selected columns and cleaning operations produce the expected prepared dataset. | Stop execution if transformation fails or the output does not match the selected preparation configuration. |
| Validate Output | The output exists, is non-empty, has the expected schema and row count, and passes the configured integrity checks. | Stop execution when an assertion fails, the output is missing or empty, or validation results differ from expectations. Do not force a failed validation to pass. |
| Record Lineage | The selected source is linked to its exact prepared output with relevant fingerprints and execution metadata. | Report or stop when source-output mappings, fingerprints or required metadata are missing or inconsistent. |

## 10. V1 Pipeline Completion Evidence

The selected tabular pipeline was executed using the shared pipeline utilities in Cell 7 and the selected CSV pathway in Cell 8B.

The required repeatability verification in Cell 9 completed successfully.

The recorded verification confirmed:

- Source fingerprints matched between executions.
- Prepared output fingerprints matched between executions.
- Source-to-output mappings matched between executions.
- The selected tabular pipeline passed its repeatability smoke check.

This provides execution evidence for the TicketIQ V1 data pipeline.

It does not prove that the dataset is fully representative of real ITSM tickets, that all labels are correct, or that the prepared data is free from every possible privacy risk.

---

**Document status:** Week 3 C3 decision record prepared for repository review and submission.
