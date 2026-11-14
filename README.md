
# TicketIQ: Comparative Machine-Learning Models for Support Ticket Classification

**Project Domain:** IT Support / IT Service Management (ITSM)  
**Project Type:** AI Engineering Prototype  
*Status:* Week 3 Data Engineering (Parts A–C) — Completed

## 1. Project Overview

TicketIQ is a machine-learning prototype that classifies incoming support tickets into predefined categories using ticket subject and initial description.

The project develops two classification models using the same input data and target categories: a baseline model and an advanced model. Their performance is then evaluated and compared using standard classification metrics.

TicketIQ is designed as a decision-support prototype. It provides predicted ticket categories for human review; it does not automatically close tickets, execute troubleshooting actions, or modify production systems.

## 2. Problem Statement

Support teams receive tickets containing descriptions of technical issues or service requests. Staff may need to read each ticket and assign it to the appropriate category before it can be routed or handled.

Manual categorisation can be time-consuming and may be inconsistent, particularly when ticket volumes are high or category definitions overlap.

Machine-learning text classification provides a practical approach to this problem. However, model performance depends on dataset quality, text quality, category definitions, class distribution, and evaluation methods.

TicketIQ will implement two models under the same experimental conditions and compare their results rather than assume that a more advanced model will always perform better.

The project will use a public ticket dataset after its data quality, label suitability, and reuse conditions have been checked. It does not claim a measured reduction in operational workload because it is evaluated as an academic prototype.

## 3. Project Objectives

- **O1 – Baseline Model:** To develop a baseline machine-learning model to classify support tickets into predefined categories using ticket subject and description.
- **O2 – Advanced Model:** To develop an advanced machine-learning model to classify support tickets into the same predefined categories using the same input data.
- **O3 – Model Comparison:** To compare the performance of the baseline and advanced machine-learning models using standard classification evaluation metrics.

## 4. Proposed Models

| Objective | Proposed Model | Purpose |
|---|---|---|
| O1 | TF-IDF + Multinomial Naive Bayes | Establish a simple baseline for text classification. |
| O2 | TF-IDF + Linear Support Vector Classifier (LinearSVC) | Evaluate a stronger classical machine-learning classifier on the same task. |
| O3 | Comparative Evaluation | Compare both models using the same held-out test data and metrics. |

Both models will use the same selected text fields, target labels, preprocessing approach, and train/test split.

The proposed models are available through scikit-learn. They can be trained locally and do not require a paid AI API or GPU.

The final model choice remains subject to dataset inspection and experimental results.

## 5. Proposed V1 Workflow

1. Load the selected support-ticket dataset.
2. Audit missing values, duplicate records, text quality, category labels, class distribution, and reuse conditions.
3. Select valid ticket subject and initial description fields as model input.
4. Select one suitable category field as the classification target, subject to the dataset audit.
5. Clean and combine the selected text fields.
6. Remove or resolve duplicate records before creating the data split.
7. Split the dataset into training and held-out test sets using stratified sampling where possible.
8. Train O1 using TF-IDF and Multinomial Naive Bayes.
9. Train O2 using TF-IDF and LinearSVC.
10. Evaluate both models on the same held-out test set.
11. Compare accuracy, precision, recall, macro-F1, and confusion matrices.
12. Discuss the results, class-level weaknesses, limitations, and the most suitable model.

## 6. Evaluation Plan

The main comparison metrics are:

- **Accuracy:** Overall proportion of correctly classified test tickets.
- **Precision:** Proportion of predicted instances of a category that are correct.
- **Recall:** Proportion of actual instances of a category that the model correctly identifies.
- **Macro-F1:** Unweighted average of F1 scores across categories.
- **Confusion Matrix:** Shows which categories are frequently confused.

Macro-F1 and per-class precision/recall are important because a dataset may contain imbalanced categories.

Both models must be evaluated on exactly the same held-out test records. No test data may be used to fit TF-IDF vocabulary, tune model settings, or make model-selection decisions.

No performance result is assumed in advance. O2 is called the advanced model because of the selected modelling approach, not because it is guaranteed to outperform O1.

## 7. Scope Boundaries

### Included in V1

- Text-based multi-class support-ticket classification.
- Two machine-learning models for the same classification task.
- Shared dataset, target categories, and experimental split.
- Quantitative evaluation and comparison.
- Error analysis using classification reports and confusion matrices.

### Excluded from V1

- Similar-ticket retrieval or historical case search.
- Retrieval of past resolutions or troubleshooting instructions.
- Generative AI responses or chatbot functionality.
- Automatic ticket routing, closure, prioritisation, or production-system actions.
- A separate priority-prediction task.
- Deep-learning or large-language-model fine-tuning.

## 8. Dataset

**Customer Support Ticket Dataset – Kaggle**

https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset

The downloaded dataset contains 8,470 rows in total, including the header row, representing 8,469 data records.

The dataset will be used as the initial candidate for the TicketIQ classification experiments. However, the total number of records does not represent the final number of usable tickets. Further data inspection and preprocessing are required before model development.

The dataset audit will examine:
- Missing values in the selected input and target columns.
- Duplicate ticket records.
- Text quality and consistency in ticket subject and description.
- Category label consistency and class distribution.
- Records that may contain irrelevant, incomplete, or unsuitable information.
- Dataset reuse conditions and suitability for academic use.

Ticket subject and initial description are the proposed model inputs. The final target category will only be confirmed after the dataset audit.

Personal information that is not required for classification will be excluded. Records that are unsuitable for supervised learning will be handled or removed based on documented data-cleaning decisions.

The final number of usable records may be lower than 8,469 after data cleaning and validation.

## 9. Responsible AI and Data Integrity

- **Privacy:** Exclude personal identifiers such as names, email addresses, and phone numbers from model inputs and published examples.
- **Data Leakage:** Use only fields available when the ticket is first submitted. Do not use resolution text, closing notes, or other post-resolution information as input.
- **Duplicate Leakage:** Check and remove exact or near-duplicate records before splitting the data.
- **Class Imbalance:** Report macro-F1 and per-class metrics rather than relying on accuracy alone.
- **Human Oversight:** Treat predictions as suggestions for review, not guaranteed correct category assignments.
- **Limitations:** Document noisy labels, ambiguous categories, missing data, and classes that cannot be evaluated reliably.

## 10. References

[1] F. Al-Hawari and H. Barham, “A machine learning based help desk system for IT service management,” Journal of King Saud University – Computer and Information Sciences, 2021. https://doi.org/10.1016/j.jksuci.2019.04.001

[2] Microsoft / Endava proof-of-concept repository, “ITSM ticket classification.” https://github.com/pourabkarchaudhuri/itsm-ticket-classification

[3] Suraj, “Customer Support Ticket Dataset,” Kaggle. https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset

## 11. Weekly Progress

| Week | Planned Work | Expected Output | Status |
|---|---|---|---|
| W1 | Define the problem, review existing work, and identify candidate datasets. | Initial project scope and README. | Completed |
| W2 | Finalise objectives, requirements, evaluation criteria, and conceptual architecture. | Updated Week 2 specifications. | Completed |
| W3 | Download and inspect the candidate dataset; verify fields and reuse conditions. | Dataset audit notes, manifest, and preparation workflow. | Completed |
| W4 | Clean data, inspect labels and class distribution, and check duplicates and leakage risks. | Prepared dataset and cleaning decisions. | Planned |
| W5 | Implement the baseline TF-IDF + Multinomial Naive Bayes pipeline. | O1 baseline experiment. | Planned |
| W6 | Implement the TF-IDF + LinearSVC pipeline using the same experiment setup. | O2 advanced-model experiment. | Planned |
| W7 | Conduct initial evaluation and review the proposal based on feedback. | Initial model results and proposal updates. | Planned |
| W8 | Semester break; organise code, notes, and backlog. | Updated task list if needed. | Semester break |
| W9 | Tune permitted model settings using training/validation data and finalise evaluation setup. | Finalised experiment configuration. | Planned |
| W10 | Evaluate both models on the held-out test set and compare metrics. | Comparative results and confusion matrices. | Planned |
| W11 | Analyse errors, class-level performance, and limitations; run repeatability checks. | Error analysis and test records. | Planned |
| W12 | Integrate the selected model or both model outputs into a simple demonstrable prototype. | Locally runnable prototype. | Planned |
| W13 | Improve input validation, documentation, and basic logging. | Refined prototype and documentation. | Planned |
| W14 | Review privacy, data leakage, class imbalance, and human oversight safeguards. | Responsible AI review. | Planned |
| W15 | Demonstrate TicketIQ and explain the models, comparison, results, and limitations. | Final showcase and project report. | Planned |
