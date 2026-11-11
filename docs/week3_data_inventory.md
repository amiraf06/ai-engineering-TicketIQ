
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

The primary model input will consist of the ticket subject and initial description. The system is intended to predict one predefined ticket category based on the selected text.

The `Ticket Type` field is a candidate target label, subject to data-quality and label-suitability checks during the dataset audit. The final target category will be confirmed after this assessment.

`Ticket Priority` will not be treated as a separate prediction task because priority prediction is explicitly outside the scope of TicketIQ V1.

The dataset will initially support data inspection, preparation, label assessment and the development of two comparative classification models.


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

The initial dataset inspection identified the following observations:
- The dataset contains 8,469 records and 17 columns.
- No missing values were found in Ticket Subject and Ticket Description.
- No exact duplicate rows or duplicate Ticket IDs were detected.
- The Ticket Subject field contains only 16 unique values, indicating substantial repetition.
- All 8,469 ticket descriptions contain at least one placeholder matching the {...} pattern.
- The inspection identified 392 repeated description values and 144 repeated subject-description combinations after basic text normalization.
- Several representative descriptions contain unrelated text, template-based content and potentially sensitive information such as email addresses, phone numbers and postal codes.
- Initial samples suggest possible inconsistencies between ticket text and assigned Ticket Type labels. Further assessment is required before confirming the target label's suitability.
- Customer Name and Customer Email are direct identifiers and should not be included in the prepared modelling dataset.
- Outcome-related fields require leakage assessment before model training.

## 6. Limitations

This dataset represents customer support tickets, not necessarily IT incidents.

Therefore, its suitability for TicketIQ's IT Incident Intelligence scope must be treated as a limitation and justified in the project documentation.

## 7. Inspection Evidence

An initial dataset inspection was conducted using notebooks/week3_dataset_inspection.py.

The inspection covered:
- Dataset dimensions and column names.
- Data types and missing values.
- Exact duplicate rows and duplicate Ticket IDs.
- Ticket Type and Ticket Priority distributions.
- Representative ticket records.
- Text quality, including empty values, placeholder occurrences, text lengths and duplicate values.
- Repeated subject-description combinations.
- Representative samples grouped by Ticket Type.

The inspection identified potential text quality and label consistency concerns. Further label-to-text consistency assessment is required before confirming the suitability of Ticket Type as the classification target.

The original dataset remains unchanged during this inspection.
