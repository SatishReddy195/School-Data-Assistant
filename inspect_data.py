import pandas as pd
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

DATA_DIRECTORY = Path(__file__).parent / "Student_Data"


# ============================================================
# Inspect all Excel files
# ============================================================

excel_files = sorted(
    DATA_DIRECTORY.glob("*.xlsx")
)

print("=" * 70)
print("SCHOOL DATA INSPECTION")
print("=" * 70)

print(f"\nFound {len(excel_files)} Excel files.\n")


for file_path in excel_files:

    print("\n" + "-" * 70)
    print(f"FILE: {file_path.name}")
    print("-" * 70)

    try:

        # Read Excel file
        df = pd.read_excel(file_path)

        # Basic information
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        print("\nColumn Names:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nFirst 5 Rows:")
        print(df.head().to_string(index=False))

        print("\nMissing Values:")
        missing = df.isnull().sum()

        for column, count in missing.items():
            if count > 0:
                print(f"  - {column}: {count}")

        if missing.sum() == 0:
            print("  No missing values.")

    except Exception as e:

        print(f"ERROR reading {file_path.name}")
        print(e)


print("\n" + "=" * 70)
print("DATA INSPECTION COMPLETE")
print("=" * 70)