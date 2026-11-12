
import pandas as pd
from pathlib import Path

# Dataset location
FILE_PATH = Path("data/raw/customer_support_tickets.csv")
RANDOM_SEED = 42

if not FILE_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {FILE_PATH}")

# Load dataset
df = pd.read_csv(FILE_PATH)

print("===== DATASET OVERVIEW =====")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print("\nColumn names:")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE CHECK =====")
print("Exact duplicate full rows:", df.duplicated().sum())
print("Duplicate Ticket IDs:", df["Ticket ID"].duplicated().sum())

print("\n===== TICKET TYPE DISTRIBUTION =====")
print(df["Ticket Type"].value_counts(dropna=False))

print("\n===== TICKET PRIORITY DISTRIBUTION =====")
print(df["Ticket Priority"].value_counts(dropna=False))

# Text quality audit
print("\n===== TEXT QUALITY AUDIT =====")

text_columns = ["Ticket Subject", "Ticket Description"]

for col in text_columns:
    text = df[col].fillna("").astype(str)

    print(f"\n--- {col} ---")
    print("Empty values:", text.str.strip().eq("").sum())
    print(
        "Placeholder occurrences:",
        text.str.contains(r"\{[^{}]+\}", regex=True).sum()
    )
    print("Average length:", round(text.str.len().mean(), 2))
    print("Minimum length:", text.str.len().min())
    print("Maximum length:", text.str.len().max())
    print("Duplicate text values:", text.duplicated().sum())

# Normalized text duplication audit
print("\n===== DUPLICATE TICKET TEXT =====")

normalized_subject = (
    df["Ticket Subject"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

normalized_description = (
    df["Ticket Description"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

normalized_combined = normalized_subject + " " + normalized_description

print(
    "Repeated subject-description combinations:",
    normalized_combined.duplicated().sum()
)
print(
    "Unique subject-description combinations:",
    normalized_combined.nunique()
)

# Representative sample metadata (no raw ticket text printed)
print("\n===== REPRESENTATIVE SAMPLE METADATA =====")

sample = df.groupby("Ticket Type", group_keys=False).head(1)

for _, record in sample.iterrows():
    print(
        f"Category: {record['Ticket Type']} | "
        f"Subject length: {len(str(record['Ticket Subject']))} | "
        f"Description length: {len(str(record['Ticket Description']))}"
    )

# Label-to-subject consistency audit
print("\n===== LABEL-TO-SUBJECT CONSISTENCY AUDIT =====")

subject_label_table = pd.crosstab(
    normalized_subject,
    df["Ticket Type"].fillna("Missing")
)

print("Unique normalized subjects:", len(subject_label_table))
print(
    "Subjects associated with multiple labels:",
    (subject_label_table.gt(0).sum(axis=1) > 1).sum()
)
print("Number of categories:", df["Ticket Type"].nunique())

# Description-level label consistency
print("\n===== DESCRIPTION-LEVEL LABEL CONSISTENCY =====")

description_label_table = pd.DataFrame({
    "description": normalized_description,
    "label": df["Ticket Type"].fillna("Missing")
})

description_groups = description_label_table.groupby("description")["label"]
description_conflicts = description_groups.nunique() > 1

conflicting_description_groups = description_conflicts.sum()
conflicting_description_records = (
    description_label_table["description"].isin(
        description_conflicts[description_conflicts].index
    ).sum()
)

print("Description groups with multiple labels:",
      conflicting_description_groups)
print("Records in conflicting description groups:",
      conflicting_description_records)

# Combined subject-description label consistency
print("\n===== COMBINED INPUT LABEL CONSISTENCY =====")

combined_label_table = pd.DataFrame({
    "input": normalized_combined,
    "label": df["Ticket Type"].fillna("Missing")
})

combined_groups = combined_label_table.groupby("input")["label"]
combined_conflicts = combined_groups.nunique() > 1

conflicting_combined_groups = combined_conflicts.sum()
conflicting_combined_records = (
    combined_label_table["input"].isin(
        combined_conflicts[combined_conflicts].index
    ).sum()
)

print("Unique combined input groups:", combined_label_table["input"].nunique())
print("Groups with multiple labels:", conflicting_combined_groups)
print("Records in conflicting groups:", conflicting_combined_records)

print("\n===== INSPECTION COMPLETED =====")
print("Raw ticket text was not printed to the terminal.")
