**Week 3 – Data Inventory**

**1\. Data Source**

- Dataset: Customer Support Ticket Dataset
- Source: <https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset>
- Dataset author: Suraj
- File: customer_support_tickets.csv
- Format: CSV
- Total records: 8,469
- Total columns: 17

**2\. Data Structure**

The dataset contains the following columns:

1. Ticket ID
2. Customer Name
3. Customer Email
4. Customer Age
5. Customer Gender
6. Product Purchased
7. Date of Purchase
8. Ticket Type
9. Ticket Subject
10. Ticket Description
11. Ticket Status
12. Resolution
13. Ticket Priority
14. Ticket Channel
15. First Response Time
16. Time to Resolution
17. Customer Satisfaction Rating

**3\. Intended Purpose**

The dataset will be used to develop and evaluate TicketIQ's text-based support-ticket classification pipeline.

The planned model inputs are Ticket Subject and Ticket Description. The system is intended to predict one predefined ticket category from the supplied ticket text.

Ticket Type is retained as a provisional candidate target for the comparative classification experiment. The dataset audit identified label-consistency concerns, so model performance must be interpreted in light of this limitation. The audit does not establish that every conflicting record is incorrectly labelled.

Ticket Priority will not be treated as a separate prediction task because priority prediction is explicitly outside the scope of TicketIQ V1.

The dataset will support data inspection, preparation, documented quality assessment and the development of two comparative classification models, subject to the limitations identified in this inventory.

**4\. Data Access and Rights**

- Dataset source: Kaggle
- Dataset author: Suraj
- Dataset version: Version 1
- File size: 3.95 MB
- Last updated: Approximately 3 years ago, as displayed on Kaggle at the time of inspection.
- Expected update frequency: Annually
- Dataset licence: CC0 1.0 Universal (Public Domain Dedication)
- Licence reference: <https://creativecommons.org/publicdomain/zero/1.0/>

The dataset is publicly available through Kaggle under the CC0 1.0 Universal licence. The original dataset source and licence reference will be retained for documentation and traceability.


**4.1 Source Identification**

| Source ID | Dataset / Filename | Type and Purpose | Version / Date / Owner | Access and Usage Rights | Inspection Evidence |
|---|---|---|---|---|---|
| S01 | Customer Support Ticket Dataset (`customer_support_tickets.csv`) — https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset | Structured CSV dataset containing customer support ticket information. Candidate source for TicketIQ's text-based ticket classification experiment. | Version 1; 3.95 MB; last updated approximately 3 years ago, as displayed in Kaggle metadata during inspection; dataset author displayed as Suraj (`suraj520`). | Publicly available through Kaggle. Licence displayed as CC0 1.0 Universal. Licence reference: https://creativecommons.org/publicdomain/zero/1.0/ | Inspected using `notebooks/week3_dataset_inspection.py`. The source contains 8,469 records and 17 columns. Inspection covered data types, missing values, duplicates, text quality, label distribution and label consistency. |

**4.2 Requirement-to-Data Mapping**

The following mapping connects TicketIQ's Week 2 requirements to the fields and evidence available in source S01.

| Requirement ID | Requirement Focus | Relevant Source Fields / Evidence | Assessment and Limitation |
|---|---|---|---|
| FR1 | Accept ticket subject and initial description as classification input. | `Ticket Subject`, `Ticket Description` | Both required text fields exist and contain no missing values. However, the dataset represents general customer support and is not confirmed to be an ITSM dataset. |
| FR3 | Baseline classification using TF-IDF and Multinomial Naive Bayes. | `Ticket Subject`, `Ticket Description`, provisional target `Ticket Type` | The required text fields and five candidate categories are available. Target suitability and label quality remain subject to further validation. |
| FR4 | Advanced classification using TF-IDF and LinearSVC. | Same input fields and provisional target `Ticket Type` used for FR3. | The same source fields and target definition must be maintained for a fair comparison. Dataset suitability remains a limitation. |
| RAI1 | Exclude unnecessary personal identifiers from model inputs and public examples. | `Customer Name`, `Customer Email`, `Ticket Subject`, `Ticket Description` | Customer Name and Customer Email are excluded. Preparation also redacts 80 detected email patterns in descriptions. A further 102 phone-like patterns were flagged, not automatically redacted; residual personal information may remain. |
| RAI2 | Prevent data leakage from information unavailable at initial ticket submission. | `Ticket Subject`, `Ticket Description`; excluded fields include `Resolution`, `Ticket Status`, `First Response Time`, `Time to Resolution` and `Customer Satisfaction Rating`. | Only the initial ticket text is selected as model input. Post-submission and outcome-related fields are excluded from the prepared modelling dataset. |
| RAI4 | Check exact and near-duplicate records before dataset splitting. | `Ticket ID`, `Ticket Subject`, `Ticket Description`, `Ticket Type` | The source has 0 exact duplicate full rows and 0 duplicate Ticket ID values. However, the selected three-column projection contains 42 exact duplicate rows. The combined subject-description audit also identified 85 groups with multiple labels, involving 205 records. These cases must be handled before train/test splitting. |
| NFR3 | Ensure repeatable preprocessing and experiment execution. | Source CSV, preparation script, prepared CSV and `data/week3_manifest.json` | Source and output SHA-256 hashes, preparation operations and validation results are recorded in the manifest. A documented random seed and repeatable training configuration must also be maintained in the model pipeline. |

**Duplicate Count Clarification**

The source-level duplicate audit and selected-column duplicate audit measure different things:

- **0 exact duplicate full rows:** No records were identical across all 17 original columns.
- **42 exact duplicate selected rows:** After projecting the source into `Ticket Subject`, `Ticket Description` and `Ticket Type`, 42 duplicate rows were detected and retained during preparation.

These findings are not contradictory. Records can differ in excluded columns while sharing identical values across the three selected modelling columns.

The conflicting-label groups are treated as data-quality risks, not automatically confirmed mislabelled records. They must be investigated and handled before model evaluation to reduce the risk of train/test leakage.


**5\. Initial Observations**

The dataset inspection and text-quality assessment identified the following observations:

- The dataset contains 8,469 records and 17 columns.
- No missing values were found in Ticket Subject and Ticket Description.
- No exact duplicate rows or duplicate Ticket ID values were detected.
- Ticket Subject contains only 16 unique values, indicating substantial repetition.
- All 8,469 ticket descriptions contain at least one placeholder matching the {...} pattern.
- The exact duplicate-description audit identified 439 records belonging to repeated description values.
- After basic text normalization (lowercasing, trimming and whitespace normalization), 457 records belonged to repeated description groups.
- The normalized subject-description inspection identified 8,325 unique subject-description combinations.
- Several representative descriptions contain unrelated text, template-based content and potentially sensitive information such as email addresses, phone numbers and postal codes.
- All 16 unique subjects were observed with all five Ticket Type categories. This indicates that subject alone does not distinguish the assigned category in this dataset.
- A normalized description-level consistency check identified 49 repeated-description groups with multiple Ticket Type labels, involving 446 records (5.27% of the dataset).
- A combined Ticket Subject and Ticket Description consistency check identified 85 repeated input groups with multiple Ticket Type labels, involving 205 records (2.42% of the dataset).
- These conflicting-label results indicate a label-quality risk. They do not prove that every affected record is incorrectly labelled or that all other records have correct labels.
- Customer Name and Customer Email are direct identifiers and should not be included in the prepared modelling dataset.
- Outcome-related fields require leakage assessment before model training.

**6\. Limitations**

This dataset represents customer support tickets, not necessarily IT incidents. Therefore, its suitability for TicketIQ's IT Incident Intelligence scope must be treated as a limitation.

The dataset also contains repetitive and template-based text, unrelated content in some descriptions, placeholders, and evidence of conflicting labels for repeated input combinations. These issues may affect the reliability and generalisability of classification results.

Ticket Type is treated as a provisional target rather than an independently verified ground-truth label. Any model evaluation must acknowledge the observed label-quality risk.

The dataset inspection does not establish that every record is suitable for modelling. Further validation and preparation decisions will be documented in the subsequent pipeline stage.

**7\. Inspection Evidence**

Dataset inspection was conducted using notebooks/week3_dataset_inspection.py and supplementary terminal-based consistency checks.

The inspection covered:

- Dataset dimensions and column names.
- Data types and missing values.
- Exact duplicate rows and duplicate Ticket ID values.
- Ticket Type and Ticket Priority distributions.
- Representative ticket records.
- Text quality, including empty values, placeholder occurrences, text lengths and repeated values.
- Repeated subject-description combinations.
- Representative samples grouped by Ticket Type.
- Label-to-subject consistency.
- Description-level and combined subject-description label consistency.

**7.1 Data Types**

The inspection identified the following data types:

- Ticket ID: int64
- Customer Age: int64
- Customer Satisfaction Rating: float64
- The remaining 14 columns: object/string fields as reported by the inspection.

**7.2 Missing Values**

The missing-value inspection reported:

| **Column**                   | **Missing values** |
| ---------------------------- | ------------------ |
| Resolution                   | 5,700              |
| First Response Time          | 2,819              |
| Time to Resolution           | 5,700              |
| Customer Satisfaction Rating | 5,700              |
| All other columns            | 0                  |

Missing values in outcome-related fields are retained in the raw dataset at this stage. No imputation or deletion was performed during the inspection.

**7.3 Duplicate Inspection**

- Exact duplicate rows: 0
- Duplicate Ticket ID values: 0
- Exact repeated-description records: 439
- Normalized repeated-description records: 457
- Unique normalized subject-description combinations: 8,325

The duplicate-description findings are text-level observations and should not be interpreted as duplicate full records.

**7.4 Label Consistency Assessment**

The consistency assessment identified:

- 49 normalized description groups associated with multiple Ticket Type labels, involving 446 records (5.27%).
- 85 combined subject-description groups associated with multiple Ticket Type labels, involving 205 records (2.42%).

These results indicate potential label inconsistency for repeated input combinations. They do not establish that all affected records are incorrectly labelled.

**7.5 Inspection Conclusion**

The inspection identified potential text-quality and label-consistency concerns. Ticket Type is retained as a provisional candidate target for subsequent preparation and comparative model evaluation, with the identified limitations documented.

No records were automatically removed based on the label-consistency findings. The original raw dataset remains unchanged during this inspection.

The inspection findings will inform the preparation decisions and validation checks documented in the subsequent pipeline stage.

**Preparation Approach and Engineering Trade-offs**

For Week 3, a **conservative data preparation strategy** was selected over aggressive automated cleaning:

| Approach | Advantages | Risks / Trade-offs |
| :--- | :--- | :--- |
| **Conservative Cleaning (Selected)** | Preserves all 8,469 records, maintains data lineage, and prevents accidental deletion of valid ticket context. | Retains 42 exact duplicate rows and 205 records in conflicting label groups that must be handled before model training. |
| **Aggressive Cleaning** | Immediately produces a smaller, denoised dataset. | High risk of corrupting valid reference numbers or dates via broad regex rules, and risks introducing bias by dropping conflicting labels without domain verification. |

**Key Preparation Decisions:**
- **Operations Applied:** Selected the 3 required columns (`Ticket Subject`, `Ticket Description`, `Ticket Type`), trimmed leading/trailing whitespace, redacted 80 confirmed email patterns (`[REDACTED_EMAIL]`), and audited duplicates and label consistency.
- **Ambiguous Numeric Patterns (102 Phone Candidates):** Flagged for audit rather than automatically redacted so that legitimate ticket reference numbers, dates, and product codes are not accidentally destroyed.
- **Downstream Plan (Week 4):** Exact duplicate records (42 rows) and conflicting template groups (205 records) are documented in `data/week3_manifest.json` and will be resolved prior to `train_test_split` in Week 4 to prevent duplicate data leakage.
