import numpy as np
import pandas as pd
from src.config import (
    CUSTOMERS_FILE,
    LOAN_APPLICATIONS_FILE,
    LOANS_FILE,
    REPAYMENT_TRANSACTIONS_FILE,
    DELINQUENCY_SNAPSHOTS_FILE,
    COLLECTIONS_ACTIONS_FILE,
    CREDIT_POLICY_SIMULATIONS_FILE,
    DAILY_PORTFOLIO_METRICS_FILE,
    PROCESSED_DATA_DIR,
    PROJECT_ROOT,
)
CLEANING_REPORT_FILE = PROJECT_ROOT / "outputs" / "reports" / "data_cleaning_summary.csv"
def save_clean(df: pd.DataFrame, file_name: str) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_DIR / file_name, index=False)
def clean_customers(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["customer_id"]).copy()
    df["occupation_category"] = df["occupation_category"].fillna("Unknown")
    df["years_employed"] = df.groupby("employment_type")["years_employed"].transform(lambda x: x.fillna(x.median()))
    df["bank_account_age_months"] = df["bank_account_age_months"].fillna(df["bank_account_age_months"].median())
    df["age"] = df["age"].clip(lower=18, upper=70).astype(int)
    df["monthly_income"] = df["monthly_income"].clip(lower=8000, upper=500000).round(0).astype(int)
    df["credit_score"] = df["credit_score"].clip(lower=300, upper=900).astype(int)
    df["debt_to_income_ratio"] = df["debt_to_income_ratio"].clip(lower=0, upper=1).round(3)
    df["years_employed"] = df["years_employed"].clip(lower=0, upper=45).round(1)
    df["bank_account_age_months"] = df["bank_account_age_months"].clip(lower=1, upper=420).round(0).astype(int)
    df["customer_since_date"] = pd.to_datetime(df["customer_since_date"]).dt.date
    report.append(["customers", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_applications(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["application_id"]).copy()
    df["purpose_category"] = df["purpose_category"].fillna("Unknown")
    df.loc[(df["approval_status"] == "Rejected") & (df["rejection_reason"].isna()), "rejection_reason"] = "Not Documented"
    df.loc[df["approval_status"] == "Approved", "rejection_reason"] = "Not Applicable"
    df["application_date"] = pd.to_datetime(df["application_date"]).dt.date
    df["approval_date"] = pd.to_datetime(df["approval_date"], errors="coerce").dt.date
    df["requested_amount"] = df["requested_amount"].clip(lower=1000, upper=1200000).round(0).astype(int)
    df["requested_tenure_months"] = df["requested_tenure_months"].clip(lower=1, upper=60).astype(int)
    df["interest_rate_offered"] = df["interest_rate_offered"].clip(lower=8, upper=45).round(2)
    df["underwriting_score"] = df["underwriting_score"].clip(lower=0, upper=100).round(2)
    df.loc[df["approval_status"] == "Rejected", "approved_amount"] = 0
    df["approved_amount"] = df["approved_amount"].fillna(0).clip(lower=0, upper=1200000).round(0).astype(int)
    report.append(["loan_applications", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_loans(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["loan_id"]).copy()
    df["disbursement_date"] = pd.to_datetime(df["disbursement_date"])
    df["closure_date"] = pd.to_datetime(df["closure_date"], errors="coerce")
    missing_closed = (df["loan_status"] == "Closed") & (df["closure_date"].isna())
    df.loc[missing_closed, "closure_date"] = df.loc[missing_closed, "disbursement_date"] + pd.to_timedelta(df.loc[missing_closed, "tenure_months"] * 30, unit="D")
    df["disbursement_date"] = df["disbursement_date"].dt.date
    df["closure_date"] = df["closure_date"].dt.date
    df["principal_amount"] = df["principal_amount"].clip(lower=1000, upper=1200000).round(2)
    df["interest_rate"] = df["interest_rate"].clip(lower=8, upper=45).round(2)
    df["tenure_months"] = df["tenure_months"].clip(lower=1, upper=60).astype(int)
    df["emi_amount"] = df["emi_amount"].clip(lower=100, upper=200000).round(2)
    df["current_outstanding"] = df["current_outstanding"].clip(lower=0).round(2)
    df["days_past_due"] = df["days_past_due"].clip(lower=0, upper=720).astype(int)
    df["default_flag"] = df["default_flag"].astype(int)
    df["write_off_flag"] = df["write_off_flag"].astype(int)
    report.append(["loans", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_repayments(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["repayment_id"], keep="first").copy()
    df["due_date"] = pd.to_datetime(df["due_date"]).dt.date
    df["payment_date"] = pd.to_datetime(df["payment_date"], errors="coerce").dt.date
    df["due_amount"] = df["due_amount"].clip(lower=0).round(2)
    df["paid_amount"] = df["paid_amount"].clip(lower=0).round(2)
    df["days_late"] = df["days_late"].clip(lower=0, upper=720).astype(int)
    overpaid_partial = (df["payment_status"] == "Partial") & (df["paid_amount"] > df["due_amount"])
    df.loc[overpaid_partial, "paid_amount"] = df.loc[overpaid_partial, "due_amount"]
    df.loc[df["payment_status"].isin(["Paid", "Late", "Partial"]) & df["payment_method"].isna(), "payment_method"] = "Unknown"
    df.loc[df["payment_status"].isin(["Missed", "Pending"]), "payment_method"] = "Not Applicable"
    report.append(["repayment_transactions", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_snapshots(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["snapshot_date", "loan_id"], keep="last").copy()
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"]).dt.date
    df["outstanding_balance"] = df["outstanding_balance"].clip(lower=0).round(2)
    df["days_past_due"] = df["days_past_due"].clip(lower=0, upper=720).astype(int)
    df["default_flag"] = df["default_flag"].astype(int)
    df["write_off_flag"] = df["write_off_flag"].astype(int)
    report.append(["delinquency_snapshots", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_collections(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["action_id"]).copy()
    df["action_date"] = pd.to_datetime(df["action_date"]).dt.date
    df["agent_id"] = df["agent_id"].fillna("AGENT_UNKNOWN")
    df["promise_to_pay_flag"] = df["promise_to_pay_flag"].astype(int)
    df["recovered_amount"] = df["recovered_amount"].clip(lower=0).round(2)
    df["contact_attempt_number"] = df["contact_attempt_number"].clip(lower=1).astype(int)
    report.append(["collections_actions", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_policy(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["simulation_id"]).copy()
    df["predicted_approval_rate"] = df["predicted_approval_rate"].clip(lower=0, upper=1).round(4)
    df["predicted_default_rate"] = df["predicted_default_rate"].clip(lower=0, upper=1).round(4)
    df["expected_credit_loss"] = df["expected_credit_loss"].clip(lower=0).round(2)
    df["projected_revenue"] = df["projected_revenue"].clip(lower=0).round(2)
    report.append(["credit_policy_simulations", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def clean_daily_metrics(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    report = []
    before_rows = len(df)
    df = df.drop_duplicates(subset=["metric_date"]).copy()
    df["metric_date"] = pd.to_datetime(df["metric_date"]).dt.date
    count_cols = ["active_loans", "loans_30_dpd", "loans_60_dpd", "loans_90_dpd", "defaults", "write_offs"]
    amount_cols = ["new_disbursements", "collection_amount", "overdue_balance", "expected_credit_loss", "portfolio_revenue"]
    for col in count_cols:
        df[col] = df[col].clip(lower=0).astype(int)
    for col in amount_cols:
        df[col] = df[col].clip(lower=0).round(2)
    df["recovery_rate"] = df["recovery_rate"].clip(lower=0, upper=1).round(4)
    report.append(["daily_portfolio_metrics", before_rows, len(df), before_rows - len(df), int(df.isna().sum().sum())])
    return df, report
def main() -> None:
    all_report_rows = []
    customers, report = clean_customers(pd.read_csv(CUSTOMERS_FILE))
    all_report_rows.extend(report)
    save_clean(customers, "customers_clean.csv")
    applications, report = clean_applications(pd.read_csv(LOAN_APPLICATIONS_FILE))
    all_report_rows.extend(report)
    save_clean(applications, "loan_applications_clean.csv")
    loans, report = clean_loans(pd.read_csv(LOANS_FILE))
    all_report_rows.extend(report)
    save_clean(loans, "loans_clean.csv")
    repayments, report = clean_repayments(pd.read_csv(REPAYMENT_TRANSACTIONS_FILE))
    all_report_rows.extend(report)
    save_clean(repayments, "repayment_transactions_clean.csv")
    snapshots, report = clean_snapshots(pd.read_csv(DELINQUENCY_SNAPSHOTS_FILE))
    all_report_rows.extend(report)
    save_clean(snapshots, "delinquency_snapshots_clean.csv")
    collections, report = clean_collections(pd.read_csv(COLLECTIONS_ACTIONS_FILE))
    all_report_rows.extend(report)
    save_clean(collections, "collections_actions_clean.csv")
    policy, report = clean_policy(pd.read_csv(CREDIT_POLICY_SIMULATIONS_FILE))
    all_report_rows.extend(report)
    save_clean(policy, "credit_policy_simulations_clean.csv")
    daily_metrics, report = clean_daily_metrics(pd.read_csv(DAILY_PORTFOLIO_METRICS_FILE))
    all_report_rows.extend(report)
    save_clean(daily_metrics, "daily_portfolio_metrics_clean.csv")
    cleaning_summary = pd.DataFrame(
        all_report_rows,
        columns=["table_name", "raw_rows", "clean_rows", "rows_removed", "remaining_missing_values"],
    )
    CLEANING_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaning_summary.to_csv(CLEANING_REPORT_FILE, index=False)
    print("Clean processed datasets created successfully")
    print(f"Processed folder: {PROCESSED_DATA_DIR}")
    print(f"Cleaning summary: {CLEANING_REPORT_FILE}")
    print("")
    print(cleaning_summary.to_string(index=False))
if __name__ == "__main__":
    main()
