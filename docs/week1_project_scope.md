
# TicketIQ: Comparative Machine-Learning Models for Support Ticket Classification

**Status:** Revised Initial Project Proposal — Dataset and Target-Label Suitability Require Validation

## 1. Project Name and Domain

TicketIQ is an AI Engineering project in the IT support / IT Service Management (ITSM) domain. It focuses on classifying support-ticket text into predefined categories using machine-learning models.

## 2. Problem Statement

Support teams receive tickets describing technical issues or service requests. Before a ticket can be handled or routed, support staff may need to read its subject and description and assign an appropriate category.

Manual categorisation can take time and may be inconsistent, particularly when ticket descriptions are unclear or category definitions overlap.

Machine-learning text classification provides a practical approach to supporting this task. However, model performance depends on the quality of the ticket text, consistency of category labels, class distribution, and experimental design.

TicketIQ will investigate this problem by developing two machine-learning classifiers for the same ticket-category prediction task. A baseline model will first be developed, followed by an advanced classical machine-learning model.

Both models will be evaluated using the same data and test set so that their performance can be compared fairly.

The project is an academic decision-support prototype. It does not claim a measured operational improvement in a specific organisation and will not autonomously manage support tickets.

## 3. Evidence of the Problem

- **Research Evidence:** Al-Hawari and Barham describe a machine-learning help-desk system for ticket classification. In their reported experiment, including ticket comments and descriptions improved prediction accuracy from 53.8% to 81.4%. This is a result from their study, not a performance claim for TicketIQ [1].
- **Engineering Example:** A public Microsoft/Endava proof-of-concept reports a help-desk ticket-classification task and describes around 50,000 labelled support tickets used for the project. It is an example of an existing workflow, not a survey proving that every support team has the same problem [2].
- **Project Implication:** Existing work demonstrates that support-ticket classification is a relevant machine-learning task. TicketIQ will focus on a controlled comparison between two classical text-classification models using one consistent dataset and evaluation procedure.

## 4. Initial Related Work

| Related Work / Solution | What It Already Does | Relevance to This Project |
|---|---|---|
| Al-Hawari & Barham (2021) [1] | Uses machine learning to classify help-desk tickets. | Supports the relevance of applying machine learning to ticket classification. |
| Microsoft / Endava ITSM Proof-of-Concept [2] | Demonstrates text preparation and ticket-field classification. | Provides an engineering example of automated ticket classification. |
| Customer Support Ticket Dataset – Kaggle [3] | Provides a public candidate dataset containing support-ticket fields. | May support a supervised classification experiment, subject to data-quality and label-suitability checks. |

## 5. Engineering Gap / Limitation

The project does not claim that no ticket-classification systems exist. Its practical engineering focus is to implement and evaluate two machine-learning approaches under the same experimental conditions.

The project will investigate whether a more advanced classical machine-learning classifier provides better classification performance than a simple baseline on the selected dataset.

The comparison will use identical input fields, target categories, data partitions, and evaluation metrics.

The result cannot be assumed in advance. The advanced model may perform better, similarly, or worse than the baseline. TicketIQ will report the measured results and discuss possible reasons for the observed differences.

## 6. Project Objectives

- **O1 – Baseline Model:** To develop a baseline machine-learning model to classify support tickets into predefined categories using ticket subject and description.
- **O2 – Advanced Model:** To develop an advanced machine-learning model to classify support tickets into the same predefined categories using the same input data.
- **O3 – Model Comparison:** To compare the performance of the baseline and advanced machine-learning models using standard classification evaluation metrics.

## 7. Proposed Models and Technical Approach

| Objective | Proposed Approach | Explanation |
|---|---|---|
| O1 | TF-IDF + Multinomial Naive Bayes | A simple and computationally efficient baseline suited to text features. |
| O2 | TF-IDF + Linear Support Vector Classifier (LinearSVC) | A classical discriminative classifier that learns decision boundaries between ticket categories. |
| O3 | Comparative Evaluation | Both models are tested on the same held-out test records. |

TF-IDF is the proposed text representation for both models. The selected text fields, cleaning steps, target labels, and data split will remain consistent.

Any model tuning will use training/validation data only; the held-out test set will be reserved for final evaluation.

The proposed methods are selected to keep the project feasible within one semester. They can be implemented using scikit-learn and do not require paid AI APIs or GPU-based training.

## 8. Target Users

- IT help-desk agents.
- IT support teams reviewing and categorising incoming support tickets.

The system is intended to provide a predicted category for human review. It will not automatically close incidents, modify production systems, execute fixes, or make final operational decisions.

## 9. Data Sources

### 9.1 Customer Support Ticket Dataset – Kaggle

https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset

The uploader describes more than 8,000 tickets with fields such as subject, description, ticket type, priority, and resolution [3].

The public description does not establish that these are authentic organisational ITSM records. The CSV must be audited for missing values, duplicates, inconsistent or noisy labels, class distribution, text quality, and licensing.

The target category must not be finalised until this audit is complete. Personal fields such as names and email addresses must be excluded from model inputs.

### 9.2 Microsoft / Endava ITSM Ticket-Classification Project

https://github.com/pourabkarchaudhuri/itsm-ticket-classification

Its README describes around 50,000 labelled support tickets from an internal help-desk source, anonymised for the public proof-of-concept [2].

Confirm current download availability and data reuse terms before considering it as an alternative dataset.

### 9.3 Incident Management Process Enriched Event Log – UCI

https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log

UCI reports 24,918 incidents, 141,712 events, and a CC BY 4.0 licence. UCI states that textual-information attributes are not included [4].

This dataset is therefore not suitable as the main text-classification dataset for TicketIQ.

## 10. Scope Boundaries

### Included

1. Text-based multi-class classification of support tickets.
2. Use of ticket subject and initial description as model input, subject to dataset audit.
3. Development of one baseline and one advanced machine-learning classifier.
4. Evaluation of both models using the same held-out test set.
5. Comparison of overall and per-class performance.
6. A simple prototype to demonstrate category predictions.

### Excluded

1. Similar-ticket retrieval or historical case search.
2. Display of historical resolutions or troubleshooting instructions.
3. Generative AI or chatbot-based troubleshooting.
4. Automatic ticket routing, closure, or execution of fixes.
5. A separate priority-prediction task.
6. Deep-learning or large-language-model fine-tuning.

## 11. Responsible AI Risks

1. **Privacy:** Public support-ticket data may contain names, emails, or other personal information. Inspect and remove personal fields, avoid using them as model inputs, and do not expose them in published examples.
2. **Data Leakage:** Do not use post-resolution text, closing notes, or fields unavailable when a new ticket arrives as input for predicting its initial category.
3. **Duplicate Leakage:** Check and remove exact or near-duplicate records before splitting data.
4. **Class Imbalance:** Rare categories may be poorly classified. Report macro-F1 and per-class precision, recall, and F1 rather than relying only on accuracy.
5. **Human Oversight:** Treat predicted categories as suggestions for review.
6. **Dataset Limitations:** Document synthetic-looking records, inconsistent labels, missing values, and categories with insufficient examples.

## References

[1] F. Al-Hawari and H. Barham, “A machine learning based help desk system for IT service management,” Journal of King Saud University – Computer and Information Sciences, 2021. https://doi.org/10.1016/j.jksuci.2019.04.001

[2] Microsoft / Endava proof-of-concept repository, “ITSM ticket classification.” https://github.com/pourabkarchaudhuri/itsm-ticket-classification

[3] Suraj, “Customer Support Ticket Dataset,” Kaggle. https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset

[4] C. Amaral, M. Fantinato, and S. Peres, “Incident management process enriched event log,” UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log
