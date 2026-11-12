
# Week 3 – Data Inventory

## 1. Data Source

- Dataset: Customer Support Ticket Dataset
- Source: https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset
- File: customer_support_tickets.csv
- Format: CSV
- Total records: 8,469
- Total columns: 17

## 2. Data Structure

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


## 3. Intended Purpose

The dataset will be used to develop and evaluate TicketIQ's text-based support-ticket classification pipeline.

The planned model inputs are Ticket Subject and Ticket Description. The system is intended to predict one predefined ticket category from the supplied ticket text.

Ticket Type is retained as a provisional candidate target for the comparative classification experiment. The dataset audit identified label-consistency concerns, so model performance must be interpreted in light of this limitation. The audit does not establish that every conflicting record is incorrectly labelled.

Ticket Priority will not be treated as a separate prediction task because priority prediction is explicitly outside the scope of TicketIQ V1.

## 4. Data Access and Rights
- Dataset source: Kaggle
- Dataset author: Suraj
- Dataset version: Version 1
- File size: 3.95 MB
- Last updated: Approximately 3 years ago, as displayed on Kaggle at the time of inspection.
- Expected update frequency: Annually
- Dataset licence: CC0 1.0 Universal (Public Domain Dedication)
- Licence reference: https://creativecommons.org/publicdomain/zero/1.0/

The dataset is publicly available through Kaggle under the CC0 1.0 Universal licence. The original dataset source and licence reference will be retained for documentation and traceability.

## 5. Initial Observations

- The dataset contains 8,469 records and 17 columns.
- No missing values were found in Ticket Subject and Ticket Description.
- No exact duplicate rows or duplicate Ticket IDs were detected.
- Ticket Subject contains only 16 unique values.
- All 8,469 descriptions contain at least one placeholder matching the {...} pattern.
- The initial text audit reported 392 repeated description values and 144 repeated subject-description combinations after basic text normalization.
- Some descriptions contain unrelated text, template-based content and potentially sensitive information such as email addresses, phone numbers and postal codes.
- All 16 unique subjects were observed with all five Ticket Type categories.
- A normalized description-level consistency check identified 49 repeated-description groups with multiple Ticket Type labels, involving 446 records (5.27%).
- A combined Ticket Subject and Ticket Description consistency check identified 85 repeated input groups with multiple Ticket Type labels, involving 205 records (2.42%).
- These findings indicate a label-quality risk. They do not prove that every affected record is incorrectly labelled or that all other records have correct labels.
- Customer Name and Customer Email are direct identifiers and should not be included in the prepared modelling dataset.
- Outcome-related fields require leakage assessment before model training.

## 6. Limitations

This dataset represents customer support tickets, not necessarily IT incidents. Therefore, its suitability for TicketIQ's IT Incident Intelligence scope must be treated as a limitation.

The dataset also contains repetitive and template-based text, unrelated content in some descriptions, placeholders, and evidence of conflicting labels for repeated input combinations. These issues may affect the reliability and generalisability of classification results.

Ticket Type is treated as a provisional target rather than an independently verified ground-truth label. Any model evaluation must acknowledge the observed label-quality risk.

## 7. Inspection Evidence

Dataset inspection was conducted using `notebooks/week3_dataset_inspection.py` and supplementary terminal-based consistency checks.

The inspection covered:

- Dataset dimensions and column names.
- Data types and missing values.
- Exact duplicate rows and duplicate Ticket IDs.
- Ticket Type and Ticket Priority distributions.
- Representative ticket records.
- Text quality, including empty values, placeholder occurrences, text lengths and repeated values.
- Repeated subject-description combinations.
- Representative samples grouped by Ticket Type.
- Label-to-subject consistency.
- Description-level and combined subject-description label consistency.

The inspection identified potential text-quality and label-consistency concerns. In particular, 205 records (2.42%) belong to repeated subject-description groups with more than one assigned Ticket Type.

These findings are documented as dataset limitations for subsequent preparation and model evaluation. They do not justify automatically deleting all affected records or assuming that every label is incorrect.

The original dataset remains unchanged during this inspection.
