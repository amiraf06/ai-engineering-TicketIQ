
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
