
import pandas as pd
from pathlib import Path

# Dataset location
file_path = Path("data/raw/customer_support_tickets.csv")

if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")

# Load dataset
df = pd.read_csv(file_path)

print("===== DATASET OVERVIEW =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nColumn names:")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE CHECK =====")
print("Exact duplicate rows:", df.duplicated().sum())
print("Duplicate Ticket IDs:", df["Ticket ID"].duplicated().sum())

print("\n===== TICKET TYPE DISTRIBUTION =====")
print(df["Ticket Type"].value_counts(dropna=False))

print("\n===== TICKET PRIORITY DISTRIBUTION =====")
print(df["Ticket Priority"].value_counts(dropna=False))

print("\n===== REPRESENTATIVE RECORDS =====")
print(
    df[["Ticket Subject", "Ticket Description", "Ticket Type"]]
    .head(5)
    .to_string(index=False)
)

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

# Combined ticket text duplication
print("\n===== DUPLICATE TICKET TEXT =====")

normalized = (
    df["Ticket Subject"].fillna("").str.lower().str.strip()
    .str.replace(r"\s+", " ", regex=True)
    + " "
    + df["Ticket Description"].fillna("").str.lower().str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

print(
    "Repeated subject-description combinations:",
    normalized.duplicated().sum()
)

# Representative samples by category
print("\n===== SAMPLE RECORDS BY TICKET TYPE =====")

for category in sorted(df["Ticket Type"].dropna().unique()):
    print(f"\n--- {category} ---")

    sample = df[df["Ticket Type"] == category][
        ["Ticket Subject", "Ticket Description"]
    ].head(3)

    for _, record in sample.iterrows():
        print("Subject:", record["Ticket Subject"])
        print("Description:", record["Ticket Description"][:400])
        print()
