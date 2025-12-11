import pandas as pd
from fuzzywuzzy import fuzz
from typing import List, Dict, Any
import os


# NOTE: Requires 'pandas' and 'fuzzywuzzy' libraries.
# Run: pip install pandas fuzzywuzzy

# --- 1. Fuzzy Matching and Normalization Helpers ---
def normalize_field(text: str) -> str:
    """
    Applies normalization logic to reduce fuzzy/near duplicates.
    Example: O -> 0, I -> 1, removing special characters.
    """
    if pd.isna(text):
        return ""
    text = str(text).upper().strip()
    # Apply common OCR/typing error corrections
    text = text.replace('O', '0')
    text = text.replace('I', '1')
    text = text.replace('-', '')
    text = text.replace('.', '')
    return text


def find_fuzzy_duplicates(df: pd.DataFrame, column: str, threshold: int = 90) -> List[Dict[str, Any]]:
    """
    Detects fuzzy/near duplicates in a large column based on a similarity score.
    """
    duplicates = []
    normalized_values = df[column].apply(normalize_field)

    # Simple nested loop for demonstration; for huge files, consider blocking or LSH
    for i in range(len(df)):
        value_i = normalized_values.iloc[i]
        original_i = df[column].iloc[i]

        if not value_i: continue

        for j in range(i + 1, len(df)):
            value_j = normalized_values.iloc[j]
            original_j = df[column].iloc[j]

            # Calculate fuzzy ratio after normalization
            ratio = fuzz.ratio(value_i, value_j)

            if ratio >= threshold:
                duplicates.append({
                    "Duplicate Type": "Fuzzy Match",
                    "Score": ratio,
                    "Item A (Row)": df.index[i],
                    "Item A (Value)": original_i,
                    "Item B (Row)": df.index[j],
                    "Item B (Value)": original_j,
                    "Normalized A": value_i,
                    "Normalized B": value_j
                })
    return duplicates


# --- 2. Proprietary Audit Rule Engine ---
def apply_proprietary_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies custom business rules to flag violating rows.
    """
    # Create a column for violation details
    df['Violation_Trigger'] = ""

    # Rule 1: Flag if 'ItemValue' is unusually high (> 5000) for 'Parcel'.
    rule_1_mask = (df['ItemType'] == 'Parcel') & (df['ItemValue'] > 5000)
    df.loc[rule_1_mask, 'Violation_Trigger'] += " | R1: High Parcel Value"

    # Rule 2: Flag if 'ShipDate' is more than 90 days ago. (Example logic)
    df['ShipDate'] = pd.to_datetime(df['ShipDate'], errors='coerce')
    cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=90)
    rule_2_mask = df['ShipDate'] < cutoff_date
    df.loc[rule_2_mask, 'Violation_Trigger'] += " | R2: Aged Shipment"

    # Clean up the violation column
    df['Violation_Trigger'] = df['Violation_Trigger'].str.strip(' | ')

    # Filter for violations
    violations_df = df[df['Violation_Trigger'] != ""].copy()
    return violations_df[['FileNumber', 'ItemType', 'ItemValue', 'Violation_Trigger']]


# --- 3. Main Audit Pipeline ---
def run_excel_audit(file_path: str):
    """
    Loads a huge Excel file (simulated) and runs all auditing checks.
    """
    print("--- Phase 3: Starting Excel Audit Engine ---")

    # --- SIMULATION: Create a mock large DataFrame ---
    # In a real scenario, this would be pd.read_excel(file_path)
    mock_data = {
        'FileNumber': ['123550', '9987', '12345O', '123550', '9987', '678I'],
        'ItemType': ['Ocean', 'Parcel', 'Ocean', 'Parcel', 'Parcel', 'Ocean'],
        'ItemValue': [15000, 4500, 3200, 15000, 6000, 7500],
        'ShipDate': ['2025-01-01', '2025-10-01', '2025-11-20', '2025-01-01', '2024-06-01', '2025-09-01']
    }
    df = pd.DataFrame(mock_data)

    print(f"Loaded DataFrame with {len(df)} rows (Simulated)")

    # 1. Exact Duplicates (FileNumber)
    exact_duplicates = df[df.duplicated(subset=['FileNumber'], keep=False)].sort_values(by='FileNumber')
    exact_report_file = "audit_report_exact_duplicates.csv"
    exact_duplicates.to_csv(exact_report_file, index=False)
    print(f"\n[DONE] Exact Duplicates Report saved to: {exact_report_file}")

    # 2. Fuzzy Duplicates (FileNumber)
    fuzzy_duplicates_list = find_fuzzy_duplicates(df, 'FileNumber', threshold=90)
    df_fuzzy = pd.DataFrame(fuzzy_duplicates_list)
    fuzzy_report_file = "audit_report_fuzzy_duplicates.csv"
    df_fuzzy.to_csv(fuzzy_report_file, index=False)
    print(f"[DONE] Fuzzy Duplicates Report saved to: {fuzzy_report_file}")

    # 3. Proprietary Rule Violations
    violations_df = apply_proprietary_rules(df)
    violations_report_file = "audit_report_violations.csv"
    violations_df.to_csv(violations_report_file, index=False)
    print(f"[DONE] Proprietary Violations Report saved to: {violations_report_file}")


if __name__ == "__main__":
    # Simulate the audit on a large Excel file
    # In a real environment, you'd pass the actual file path.
    # We are using a mock path here.
    MOCK_EXCEL_PATH = "huge_audit_file.xlsx"
    run_excel_audit(MOCK_EXCEL_PATH)
