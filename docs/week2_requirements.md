
# TicketIQ: Project Framing, Application Scope, and Requirements Specification

**Version:** 2.0  
**Status:** Revised Week 2 Engineering Specification

---

## Section 0 - Project Framing & Application Scope Checkpoint

| Framing Element | TicketIQ Specification |
|---|---|
| Problem + Evidence | Support teams receive tickets containing technical issues or service requests. Staff may need to read each ticket and assign a category before routing or handling it. Manual categorisation can be time-consuming and inconsistent. Al-Hawari and Barham (2021) investigated machine-learning ticket classification in a help-desk workflow [1]. A Microsoft/Endava proof-of-concept also documents automated ticket classification as an ITSM use case [2]. |
| Existing Approaches | 1. Al-Hawari & Barham (2021) [1]: Supervised machine learning for help-desk ticket classification. 2. Microsoft / Endava [2]: Text preprocessing and ticket-field classification. 3. Public support-ticket datasets [3]: Candidate data for supervised text-classification experiments. |
| Project / Engineering Gap | Ticket classification is an established task. TicketIQ's engineering focus is to implement two classical machine-learning models for the same text-classification problem and compare them under a controlled and reproducible experiment. |
| Objective O1 | To develop a baseline machine-learning model to classify support tickets into predefined categories using ticket subject and description. |
| Objective O2 | To develop an advanced machine-learning model to classify support tickets into the same predefined categories using the same input data. |
| Objective O3 | To compare the performance of the baseline and advanced machine-learning models using standard classification evaluation metrics. |
| Intended Users | IT help-desk agents and IT support staff who review and categorise incoming support tickets. |
| Supported Tasks | 1. Accept ticket subject and initial description text. 2. Process text into machine-learning features. 3. Predict one predefined ticket category. 4. Compare baseline and advanced model outputs during evaluation. 5. Present the predicted category as a suggestion for human review. |
| Information / Knowledge Domain | Public support-ticket datasets containing initial ticket text and a suitable category label. The Kaggle Customer Support Ticket Dataset [3] is a candidate and must pass data-quality and label-suitability checks. |
| Operating Context | A local or locally runnable academic prototype used to demonstrate text-based ticket categorisation. A human user reviews the predicted category. |
| Important Constraints | 1. Dataset text fields and category labels must be audited. 2. Both models must use the same input fields, target categories, and data partitions. 3. Only information available at initial ticket submission may be used. 4. Prefer classical scikit-learn models that run locally. 5. The project must remain feasible within one semester. |
| Explicit Out-of-Scope Tasks | 1. Similar-ticket retrieval and historical case search. 2. Displaying historical resolutions. 3. Generating fixes using a language model or chatbot. 4. Automatically routing, closing, prioritising, or modifying production tickets. 5. Priority prediction as a separate task. 6. Deep-learning or large-language-model fine-tuning. |
| Evaluation Focus | Evaluate the baseline model, evaluate the advanced model on the same held-out test records, and compare their overall and per-class results using accuracy, precision, recall, macro-F1, and confusion matrices. |

---

## Section 1 - Functional Requirements

| ID | Requirement - The System SHALL | Scope Boundary - SHALL NOT |
|---|---|---|
| FR1 | Accept a support ticket's subject and initial description as text input for classification. | Require resolution notes, closing comments, or other post-resolution information for prediction. |
| FR2 | Preprocess the selected ticket text and transform it into numerical features using the agreed text-representation method, initially TF-IDF. | Fit preprocessing vocabulary or feature weights using held-out test data. |
| FR3 | Provide a baseline classification model using TF-IDF features and Multinomial Naive Bayes, subject to dataset compatibility. | Use a different target-label definition or test split from the advanced model. |
| FR4 | Provide an advanced classification model using TF-IDF features and LinearSVC, subject to dataset suitability. | Use additional input fields or test records unavailable to the baseline model. |
| FR5 | Evaluate both models on the same held-out test records and produce comparable classification metrics and confusion matrices. | Use the held-out test set for fitting TF-IDF, model training, or hyperparameter selection. |
| FR6 | Accept valid non-empty ticket text and provide a predicted category from the predefined target classes. | Automatically route, close, prioritise, or modify a real support ticket. |

---

## Section 2 - Non-Functional Requirements

| ID | Quality Attribute | Requirement | Measurement Method | Metric | Acceptance Target |
|---|---|---|---|---|---|
| NFR1 | Classification Quality | Both models shall be evaluated using standard multi-class classification metrics on the same held-out test set. | Generate a classification report for each model. | Accuracy, macro precision, macro recall, macro-F1 | Report all metrics for both models. |
| NFR2 | Fairness of Comparison | Both models shall use the same input fields, target labels, data split, and test records. | Compare experiment configuration and test-record indices. | Configuration consistency | Same held-out test records and target-label mapping. |
| NFR3 | Reproducibility | The experiment shall use a documented random seed and repeatable preprocessing/training pipeline. | Re-run the experiment using the documented configuration. | Reproducibility of split and metrics | Same data split and materially consistent results under the documented environment. |
| NFR4 | Performance | The prototype shall return a category prediction within a practical interactive response time on the target local environment. | Measure prediction latency over test inputs after model loading. | Median and p90 prediction latency | Record actual results and environment; set a numeric target after the first prototype. |
| NFR5 | Cost | Model development and inference shall avoid paid external AI APIs. | Review dependencies and record external API usage. | External AI/API cost | US$0.00 external AI/API usage for the core workflow. |

---

## Section 3 - Responsible AI Requirements

| ID | Responsible AI Risk | Requirement | Measurement Method | Metric | Acceptance Target |
|---|---|---|---|---|---|
| RAI1 | Privacy | Personal identifiers not required for classification shall be excluded from model inputs and public output examples. | Inspect selected columns and processed records. | Personal-identifier fields used as input | 0 unnecessary personal-identifier fields. |
| RAI2 | Data Leakage | Models shall use only ticket information available at initial submission time. | Audit input feature list and data pipeline. | Post-submission fields used as input | 0 post-submission fields. |
| RAI3 | Class Imbalance | Evaluation shall report class-level performance so that weak minority-category performance is not hidden by accuracy. | Generate per-class precision, recall, F1, support, and confusion matrix. | Completeness of per-class reporting | 100% of evaluable target classes included. |
| RAI4 | Data Integrity | Exact and near-duplicate records shall be checked before splitting the dataset. | Run duplicate checks and inspect cross-split overlap. | Known duplicate overlap across train/test | 0 known exact-duplicate records across splits after cleaning. |
| RAI5 | Human Oversight | Predicted categories shall be presented as model outputs for human review, not guaranteed decisions. | Review interface wording and workflow. | Presence of human-review notice | Predictions labelled as suggestions; no automatic ticket action. |

---

## Part A Reflection

**Question:** Which Responsible AI requirement in your project will be the most difficult to measure or enforce technically? Why?

**Reflection:**

The most difficult Responsible AI requirement to evaluate is RAI3 (Class Imbalance). A model may achieve high overall accuracy by correctly predicting common categories while performing poorly on less frequent categories. This is important because a support-ticket classifier should not hide weak performance on minority categories behind one overall score.

TicketIQ will therefore report macro-F1, per-class precision, recall, F1, and a confusion matrix for both models. However, some categories may contain too few examples for a stable evaluation. If this occurs, the limitation will be documented rather than presenting an unreliable class-level result as conclusive.

## References

[1] F. Al-Hawari and H. Barham, “A machine learning based help desk system for IT service management,” Journal of King Saud University – Computer and Information Sciences, vol. 33, no. 6, pp. 702-718, 2021. https://doi.org/10.1016/j.jksuci.2019.04.001

[2] Microsoft / Endava, “ITSM ticket classification proof-of-concept repository,” GitHub. https://github.com/pourabkarchaudhuri/itsm-ticket-classification

[3] Suraj, “Customer Support Ticket Dataset,” Kaggle. https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset
