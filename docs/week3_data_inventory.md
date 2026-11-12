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
