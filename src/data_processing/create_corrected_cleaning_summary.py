import pandas as pd
from src.config import PROCESSED_DATA_DIR, PROJECT_ROOT
CORRECTED_SUMMARY_FILE = PROJECT_ROOT / "outputs" / "reports" / "data_cleaning_summary_corrected.csv"
FILES = {
    "customers": "customers_clean.csv",
    "loan_applications": "loan_applications_clean.csv",
    "loans": "loans_clean.csv",
    "repayment_transactions": "repayment_transactions_clean.csv",
    "delinquency_snapshots": "delinquency_snapshots_clean.csv",
    "collections_actions": "collections_actions_clean.csv",
    "credit_policy_simulations": "credit_policy_simulations_clean.csv",
    "daily_portfolio_metrics": "daily_portfolio_metrics_clean.csv",
}
ALLOWED_NULL_COLUMNS = {
    "loan_applications": ["approval_date"],
    "loans": ["closure_date"],
    "repayment_transactions": ["payment_date"],
}
def main() -> None:
    summary_rows = []
    for table_name, file_name in FILES.items():
        df = pd.read_csv(PROCESSED_DATA_DIR / file_name)
        total_nulls = int(df.isna().sum().sum())
        allowed_nulls = 0
        for col in ALLOWED_NULL_COLUMNS.get(table_name, []):
            if col in df.columns:
                allowed_nulls += int(df[col].isna().sum())
        problem_nulls = total_nulls - allowed_nulls
        summary_rows.append(
            {
                "table_name": table_name,
                "rows": len(df),
                "columns": df.shape[1],
                "total_null_values": total_nulls,
                "allowed_business_nulls": allowed_nulls,
                "problem_null_values": problem_nulls,
                "status": "PASS" if problem_nulls == 0 else "REVIEW",
            }
        )
    summary = pd.DataFrame(summary_rows)
    CORRECTED_SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(CORRECTED_SUMMARY_FILE, index=False)
    print("Corrected cleaning summary created successfully")
    print(f"Output file: {CORRECTED_SUMMARY_FILE}")
    print("")
    print(summary.to_string(index=False))
    print("")
    print("Total problem null values:", int(summary["problem_null_values"].sum()))
if __name__ == "__main__":
    main()
