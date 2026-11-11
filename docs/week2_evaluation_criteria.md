
# TicketIQ: Evaluation Criteria Specification

**Version:** 2.0  
**Status:** Revised Week 2 Evaluation Plan

---

## 1. Evaluation Overview

TicketIQ has three connected objectives:

- **O1:** Develop a baseline machine-learning model to classify support tickets into predefined categories using ticket subject and description.
- **O2:** Develop an advanced machine-learning model to classify support tickets into the same predefined categories using the same input data.
- **O3:** Compare the performance of the baseline and advanced machine-learning models using standard classification evaluation metrics.

The evaluation will compare two models for one classification task. It will not evaluate ticket retrieval, historical resolution relevance, or abstention behaviour because these functions are outside the revised project scope.

## 2. Proposed Model Evaluation

| Objective / Requirement ID | Evaluation Criterion | Model / Capability | Measurement Method | Metric | Reporting Target |
|---|---|---|---|---|---|
| O1 / FR3 | Baseline Classification Performance | TF-IDF + Multinomial Naive Bayes | Train the baseline model and evaluate on the held-out test set. | Accuracy, macro precision, macro recall, macro-F1, confusion matrix | Report all metrics and per-class results. |
| O2 / FR4 | Advanced Classification Performance | TF-IDF + LinearSVC | Train the advanced model and evaluate on the same held-out test set. | Accuracy, macro precision, macro recall, macro-F1, confusion matrix | Report all metrics and per-class results. |
| O3 / FR5 / NFR2 | Model Performance Comparison | Baseline vs Advanced | Compare both models using identical test records and category labels. | Difference in accuracy, macro precision, macro recall, macro-F1; per-class comparison | Present side-by-side results and explain differences. |
| NFR3 / NFR4 | Reproducibility and Prediction Performance | Both models | Repeat the documented experiment and measure inference time. | Reproducibility check; median and p90 prediction latency | Record actual results and environment. |
| RAI1 / RAI2 / RAI4 | Privacy, Leakage, and Data Integrity | Shared data pipeline | Inspect model input columns, processed samples, duplicate checks, and train/test separation. | Personal fields used; post-submission fields used; duplicate overlap | 0 unnecessary personal fields and 0 post-submission fields used as input. |

## 3. Classification Metrics

### 3.1 Accuracy

Accuracy measures the proportion of all test records that are classified correctly.

Accuracy = Number of Correct Predictions / Total Number of Predictions

Accuracy provides an overall view but may be misleading when some ticket categories are much more common than others.

### 3.2 Precision

Precision measures how many records predicted as a particular category actually belong to that category.

Precision = TP / (TP + FP)

Low precision means the model frequently assigns a category to tickets that do not belong to it.

### 3.3 Recall

Recall measures how many actual records from a category are correctly identified by the model.

Recall = TP / (TP + FN)

Low recall means the model misses many tickets belonging to that category.

### 3.4 F1-score and Macro-F1

F1-score is the harmonic mean of precision and recall.

F1 = 2 × (Precision × Recall) / (Precision + Recall)

Macro-F1 calculates the F1-score for each category and then takes the unweighted average. Each category contributes equally, making macro-F1 useful when the dataset contains imbalanced classes.

### 3.5 Confusion Matrix

A confusion matrix shows the actual category against the predicted category. It helps identify which categories are correctly classified and which categories are commonly confused with one another.

## 4. Fair Experimental Comparison

To make the comparison meaningful, both models must follow the same experimental conditions:

1. Use the same audited dataset.
2. Use the same ticket subject and description fields.
3. Use the same target category column and category-label mapping.
4. Apply the same text-cleaning procedure.
5. Remove or resolve duplicates before splitting the data.
6. Use the same stratified training and held-out test split where class counts permit.
7. Fit TF-IDF only on training data within each model pipeline.
8. Use the same held-out test records for final evaluation.
9. Do not tune model parameters using held-out test results.
10. Report the software environment and random seed.

If a validation set is used for hyperparameter tuning, it must be separated from the final test set. The final test set must be used only for final evaluation.

## 5. Proposed Experiment Sequence

| Step | Activity | Expected Evidence |
|---|---|---|
| 1 | Audit and select the dataset and target category. | Dataset audit report and selected column list. |
| 2 | Prepare ticket subject and description text. | Reproducible preprocessing pipeline. |
| 3 | Remove duplicates and create training/test partitions. | Split indices and data-integrity checks. |
| 4 | Train TF-IDF + Multinomial Naive Bayes. | Trained O1 pipeline and baseline predictions. |
| 5 | Train TF-IDF + LinearSVC. | Trained O2 pipeline and advanced predictions. |
| 6 | Evaluate both models on the same test set. | Classification reports and confusion matrices. |
| 7 | Compare results and inspect errors. | Comparative results table and error analysis. |

## 6. Result Interpretation

The advanced model must not be assumed to outperform the baseline.

- **O2 performs better:** Discuss which categories benefit and whether improvement is consistent across classes.
- **Both models perform similarly:** The simpler baseline may be sufficient for the selected dataset.
- **O1 performs better:** The advanced model may not suit the dataset or its settings may require further investigation.
- **Both models perform poorly:** The dataset may have noisy labels, ambiguous categories, insufficient examples, or weak text features.

The final model recommendation should consider macro-F1, per-class performance, confusion patterns, and computational practicality, not accuracy alone.

---

## Part B Reflection

**Question:** Which evaluation criterion is most important for determining whether your AI application will be useful to its intended users? Why?

**Reflection:**

The most important evaluation criterion for TicketIQ is Macro-F1, supported by per-class precision, recall, and the confusion matrix.

Overall accuracy is useful, but it can hide poor performance on less frequent ticket categories. If the classifier performs well only on common categories, its usefulness to support staff may be limited when less common issues appear.

Macro-F1 gives each category equal weight, while per-class metrics and the confusion matrix show where the models make mistakes.

Comparing these results for both models on the same held-out test set provides a more balanced basis for deciding which approach is more suitable.

Nevertheless, no single metric proves that the prototype is ready for operational deployment. Predictions still require human review and dataset limitations must be considered.
