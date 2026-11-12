
"""
TicketIQ - Week 3 Part B
Data Preparation Pipeline

Purpose:
1. Load the original dataset.
2. Select relevant features and target.
3. Inspect missing values.
4. Apply conservative text cleaning.
5. Redact obvious email addresses.
6. Validate target labels.
7. Audit duplicate and conflicting-label records.
8. Export the prepared dataset.
9. Generate a SHA256-based data preparation manifest.

Important:
- The raw dataset is never modified.
- Duplicate records are retained.
- Conflicting labels are not automatically corrected.
"""

from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

import pandas as pd


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" /
    "customer_support_tickets.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_PATH = (
    PROCESSED_DIR / "ticketiq_dataset.csv"
)

MANIFEST_PATH = (
    PROJECT_ROOT / "data" / "week3_manifest.json"
)

SELECTED_COLUMNS = [
    "Ticket Subject",
    "Ticket Description",
    "Ticket Type"
]

EXPECTED_LABELS = [
    "Refund request",
    "Technical issue",
    "Cancellation request",
    "Product inquiry",
    "Billing inquiry"
]

EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE
)

PHONE_CANDIDATE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?\d[\d\s().-]{6,}\d)(?!\w)"
)


# ============================================================
# 2. UTILITY FUNCTIONS
# ============================================================

def calculate_sha256(file_path):
    """Calculate SHA256 hash for a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024), b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def normalize_text(value):
    """
    Normalize text only for audit comparisons.

    This function does not modify the actual dataset.
    """

    return re.sub(
        r"\s+",
        " ",
        str(value).strip().casefold()
    )


def count_email_addresses(value):
    """Count email addresses in a text value."""

    return len(EMAIL_PATTERN.findall(str(value)))


def redact_emails(value):
    """Replace obvious email addresses with a placeholder."""

    return EMAIL_PATTERN.sub(
        "[REDACTED_EMAIL]",
        str(value)
    )


def count_phone_candidates(value):
    """
    Count possible phone-number patterns.

    These are flagged only. They are not automatically
    replaced because numeric patterns may represent
    dates, order numbers or other references.
    """

    count = 0

    for match in PHONE_CANDIDATE_PATTERN.finditer(
        str(value)
    ):
        digits = re.sub(r"\D", "", match.group())

        if 8 <= len(digits) <= 15:
            count += 1

    return count


def get_conflicting_group_statistics(
    dataframe,
    grouping_columns
):
    """
    Identify normalized input groups associated
    with more than one Ticket Type.
    """

    audit_df = dataframe.copy()

    for column in grouping_columns:
        audit_df[f"_normalized_{column}"] = (
            audit_df[column].apply(normalize_text)
        )

    normalized_columns = [
        f"_normalized_{column}"
        for column in grouping_columns
    ]

    grouped = (
        audit_df.groupby(
            normalized_columns,
            dropna=False
        )["Ticket Type"]
        .agg(["nunique", "size"])
    )

    conflicting_groups = grouped[
        grouped["nunique"] > 1
    ]

    return {
        "total_unique_input_groups": int(len(grouped)),
        "groups_with_multiple_labels": int(
            len(conflicting_groups)
        ),
        "records_in_conflicting_groups": int(
            conflicting_groups["size"].sum()
        )
    }


# ============================================================
# 3. VERIFY SOURCE DATASET
# ============================================================

print("=" * 65)
print("TICKETIQ - WEEK 3 PART B DATA PREPARATION")
print("=" * 65)

if not RAW_DATA_PATH.exists():
    raise FileNotFoundError(
        f"Raw dataset not found: {RAW_DATA_PATH}"
    )

print("\n[1/8] Source dataset verification")

source_hash = calculate_sha256(RAW_DATA_PATH)

print(f"Source file: {RAW_DATA_PATH.name}")
print(f"Source SHA256: {source_hash}")


# ============================================================
# 4. LOAD ORIGINAL DATASET
# ============================================================

print("\n[2/8] Loading original dataset")

df = pd.read_csv(
    RAW_DATA_PATH,
    encoding="utf-8-sig"
)

original_row_count = len(df)
original_columns = df.columns.tolist()

print(f"Original rows: {original_row_count}")
print(f"Original columns: {len(original_columns)}")


# ============================================================
# 5. CHECK REQUIRED COLUMNS
# ============================================================

print("\n[3/8] Checking required columns")

missing_columns = [
    column
    for column in SELECTED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )

print("All required columns are available.")


# ============================================================
# 6. SELECT FEATURES AND TARGET
# ============================================================

print("\n[4/8] Selecting relevant columns")

prepared_df = df[SELECTED_COLUMNS].copy()

print("Selected columns:")

for column in SELECTED_COLUMNS:
    print(f" - {column}")


# ============================================================
# 7. MISSING VALUE VALIDATION
# ============================================================

print("\n[5/8] Checking missing values")

missing_before = {
    column: int(prepared_df[column].isna().sum())
    for column in SELECTED_COLUMNS
}

print("Missing values:")

for column, count in missing_before.items():
    print(f" - {column}: {count}")

total_missing = sum(missing_before.values())

if total_missing > 0:
    raise ValueError(
        "Missing values found in required columns. "
        "Review the source data before continuing. "
        "No automatic imputation or row deletion was applied."
    )

print("Required columns passed missing-value validation.")


# ============================================================
# 8. CONSERVATIVE TEXT CLEANING
# ============================================================

print("\n[6/8] Applying text preparation")

# Convert required fields to strings.
# Missing values have already been checked.
for column in SELECTED_COLUMNS:
    prepared_df[column] = (
        prepared_df[column].astype(str).str.strip()
    )

# Count obvious email addresses before redaction.
email_counts_before = {
    column: int(
        prepared_df[column].apply(
            count_email_addresses
        ).sum()
    )
    for column in [
        "Ticket Subject",
        "Ticket Description"
    ]
}

# Redact obvious email addresses.
for column in [
    "Ticket Subject",
    "Ticket Description"
]:
    prepared_df[column] = (
        prepared_df[column].apply(redact_emails)
    )

# Count possible phone-number patterns.
# Do not automatically redact ambiguous numeric sequences.
phone_candidate_counts = {
    column: int(
        prepared_df[column].apply(
            count_phone_candidates
        ).sum()
    )
    for column in [
        "Ticket Subject",
        "Ticket Description"
    ]
}

print("Whitespace trimming: completed")
print("Email redaction: completed")
print("Automatic phone redaction: not applied")

print("Email addresses redacted:")

for column, count in email_counts_before.items():
    print(f" - {column}: {count}")

print("Possible phone-number patterns flagged:")

for column, count in phone_candidate_counts.items():
    print(f" - {column}: {count}")


# ============================================================
# 9. TARGET LABEL VALIDATION
# ============================================================

print("\n[7/8] Validating target labels")

observed_labels = sorted(
    prepared_df["Ticket Type"].unique().tolist()
)

unexpected_labels = [
    label
    for label in observed_labels
    if label not in EXPECTED_LABELS
]

missing_expected_labels = [
    label
    for label in EXPECTED_LABELS
    if label not in observed_labels
]

if unexpected_labels:
    raise ValueError(
        f"Unexpected target labels detected: {unexpected_labels}"
    )

if missing_expected_labels:
    raise ValueError(
        f"Expected labels missing: {missing_expected_labels}"
    )

label_distribution = {
    str(label): int(count)
    for label, count in (
        prepared_df["Ticket Type"]
        .value_counts()
        .sort_index()
        .items()
    )
}

print("Target labels validated.")

for label, count in label_distribution.items():
    print(f" - {label}: {count}")


# ============================================================
# 10. DUPLICATE AUDIT
# ============================================================

print("\n[8/8] Running duplicate and label consistency audit")

# Count duplicate rows based on the three selected columns.
# Records are retained; no automatic deletion is performed.
exact_duplicate_rows = int(
    prepared_df.duplicated(
        subset=SELECTED_COLUMNS
    ).sum()
)

# Audit description-level conflicts.
description_audit = (
    get_conflicting_group_statistics(
        prepared_df,
        ["Ticket Description"]
    )
)

# Audit combined subject-description conflicts.
combined_audit = (
    get_conflicting_group_statistics(
        prepared_df,
        [
            "Ticket Subject",
            "Ticket Description"
        ]
    )
)

print(
    "Duplicate rows across selected columns:",
    exact_duplicate_rows
)

print(
    "Description groups with multiple labels:",
    description_audit[
        "groups_with_multiple_labels"
    ]
)

print(
    "Subject-description groups with multiple labels:",
    combined_audit[
        "groups_with_multiple_labels"
    ]
)

print(
    "Records in conflicting subject-description groups:",
    combined_audit[
        "records_in_conflicting_groups"
    ]
)

# All records are retained.
rows_before_preparation = len(prepared_df)


# ============================================================
# 11. OUTPUT VALIDATION
# ============================================================

print("\nPreparing output directory")

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Export prepared data.
prepared_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

# Reload exported file to verify its actual contents.
validated_df = pd.read_csv(
    OUTPUT_PATH,
    encoding="utf-8-sig"
)

output_columns_valid = (
    validated_df.columns.tolist() == SELECTED_COLUMNS
)

output_row_count_valid = (
    len(validated_df) == rows_before_preparation
)

output_missing_values = {
    column: int(validated_df[column].isna().sum())
    for column in SELECTED_COLUMNS
}

output_missing_valid = (
    sum(output_missing_values.values()) == 0
)

if not output_columns_valid:
    raise ValueError("Output column validation failed.")

if not output_row_count_valid:
    raise ValueError("Output row count validation failed.")

if not output_missing_valid:
    raise ValueError("Output missing-value validation failed.")

output_hash = calculate_sha256(OUTPUT_PATH)


# ============================================================
# 12. GENERATE DATA PREPARATION MANIFEST
# ============================================================

manifest = {
    "manifest_version": "1.0",

    "project": "TicketIQ",

    "stage": "Week 3 Part B - Data Preparation",

    "generated_at_utc": (
        datetime.now(timezone.utc).isoformat()
    ),

    "source": {
        "filename": RAW_DATA_PATH.name,
        "relative_path": "data/raw/customer_support_tickets.csv",
        "url": "https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset",
        "creator": "suraj520 (Kaggle username)",
        "version": "Version 1",
        "file_size": "3.95 MB",
        "last_updated": "3 years ago (as displayed on Kaggle)",
        "license": "CC0: Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "sha256": source_hash,
        "row_count": int(original_row_count),
        "column_count": int(len(original_columns)),
        "columns": original_columns
    },

    "preparation": {
        "selected_columns": SELECTED_COLUMNS,
        "excluded_columns": [
            column
            for column in original_columns
            if column not in SELECTED_COLUMNS
        ],

        "operations": [
            "Selected Ticket Subject, Ticket Description and Ticket Type.",
            "Trimmed leading and trailing whitespace.",
            "Redacted obvious email addresses in text fields.",
            "Flagged potential phone-number patterns without automatic redaction.",
            "Validated target labels against the expected label set.",
            "Audited duplicate records without deleting them.",
            "Audited conflicting labels without modifying them."
        ],
        
        "missing_values_before_preparation": missing_before,

        "email_redaction_counts": email_counts_before,

        "phone_candidate_counts": phone_candidate_counts,

        "duplicate_policy": (
            "Duplicate records were retained. "
            "No automatic duplicate removal was applied."
        ),

        "label_distribution": label_distribution,

        "unexpected_labels": unexpected_labels,

        "missing_expected_labels": missing_expected_labels
    },

    "quality_audit": {
        "selected_column_duplicate_rows": exact_duplicate_rows,

        "description_level_label_consistency": (
            description_audit
        ),

        "subject_description_label_consistency": (
            combined_audit
        ),

        "output_column_validation": bool(
            output_columns_valid
        ),

        "output_row_count_validation": bool(
            output_row_count_valid
        ),

        "output_missing_value_validation": bool(
            output_missing_valid
        )
    },

    "output": {
        "filename": OUTPUT_PATH.name,
        "relative_path": "data/processed/ticketiq_dataset.csv",
        "sha256": output_hash,
        "row_count": int(len(validated_df)),
        "column_count": int(len(validated_df.columns)),
        "columns": validated_df.columns.tolist()
    },

    "limitations": [
        "The source dataset is a customer support dataset, not necessarily an ITSM dataset.",
        "Conflicting labels were retained and require further investigation.",
        "Possible phone-number patterns were flagged but not automatically redacted.",
        "Potential personal information other than obvious email addresses may remain in text fields.",
        "The prepared dataset should remain local until privacy review is completed."
    ]
}

MANIFEST_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    MANIFEST_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        manifest,
        file,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("DATA PREPARATION COMPLETED")
print("=" * 65)

print(f"Original records: {original_row_count}")
print(f"Prepared records: {len(validated_df)}")
print(f"Selected columns: {len(validated_df.columns)}")
print(f"Duplicate rows retained: {exact_duplicate_rows}")

print("\nGenerated files:")

print(
    "Prepared dataset:",
    OUTPUT_PATH.relative_to(PROJECT_ROOT)
)

print(
    "Manifest:",
    MANIFEST_PATH.relative_to(PROJECT_ROOT)
)

print("\nOutput SHA256:")
print(output_hash)

print("\nValidation results:")

print(" - Column validation: PASSED")
print(" - Row count validation: PASSED")
print(" - Missing-value validation: PASSED")
print(" - Target label validation: PASSED")

print("\nPrivacy reminder:")
print(
    "Review possible personal information before "
    "sharing or committing the processed dataset."
)

print("\nWeek 3 Part B pipeline finished successfully.")
