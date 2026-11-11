
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

The dataset will be used to explore and develop the TicketIQ ticket classification pipeline.

Potential prediction targets include Ticket Priority and Ticket Type, subject to further validation against the project's requirements.

## 4. Data Access and Rights

The dataset was obtained from Kaggle.

The exact dataset licence and redistribution permissions have not yet been verified.

## 5. Initial Observations

- The dataset contains structured tabular data.
- Ticket Subject and Ticket Description may provide useful textual information.
- Ticket Priority and Ticket Type may serve as prediction targets.
- Customer Name and Customer Email are direct identifiers and should not be included in the prepared modelling dataset.
- Resolution, Ticket Status and other outcome-related fields require leakage assessment before model training.

## 6. Limitations

This dataset represents customer support tickets, not necessarily IT incidents.

Therefore, its suitability for TicketIQ's IT Incident Intelligence scope must be treated as a limitation and justified in the project documentation.

## 7. Inspection Evidence

Detailed checks for missing values, duplicate records, data types and representative records are pending.

These results will be added after dataset inspection.
