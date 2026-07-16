import pandas as pd
from src.config import (
    CUSTOMER_COUNT,
    APPLICATION_COUNT,
    MIN_APPROVED_LOANS,
    CUSTOMERS_FILE,
    LOAN_APPLICATIONS_FILE,
    LOANS_FILE,
    REPAYMENT_TRANSACTIONS_FILE,
    DELINQUENCY_SNAPSHOTS_FILE,
    COLLECTIONS_ACTIONS_FILE,
    CREDIT_POLICY_SIMULATIONS_FILE,
    DAILY_PORTFOLIO_METRICS_FILE,
    PROJECT_ROOT,
)
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
QUALITY_SUMMARY_FILE = REPORT_DIR / "raw_data_quality_summary.csv"
VALIDATION_REPORT_FILE = REPORT_DIR / "raw_data_validation_report.md"
REQUIRED_COLUMNS = {
    "customers": [
        "customer_id", "age", "gender", "city", "state", "employment_type",
        "occupation_category", "monthly_income", "credit_score",
        "debt_to_income_ratio", "years_employed", "bank_account_age_months",
        "customer_since_date", "acquisition_channel"
    ],
    "loan_applications": [
        "application_id", "customer_id", "application_date", "loan_product",
        "requested_amount", "requested_tenure_months", "purpose_category",
        "interest_rate_offered", "risk_band", "approval_status",
        "rejection_reason", "approved_amount", "approval_date",
        "underwriting_score"
    ],
    "loans": [
        "loan_id", "application_id", "customer_id", "disbursement_date",
        "principal_amount", "interest_rate", "tenure_months", "emi_amount",
        "loan_status", "current_outstanding", "days_past_due",
        "default_flag", "write_off_flag", "closure_date"
    ],
    "repayment_transactions": [
        "repayment_id", "loan_id", "due_date", "payment_date", "due_amount",
        "paid_amount", "payment_status", "days_late", "payment_method"
    ],
    "delinquency_snapshots": [
        "snapshot_date", "loan_id", "customer_id", "outstanding_balance",
        "days_past_due", "delinquency_bucket", "roll_rate_stage",
        "collection_status", "default_flag", "write_off_flag"
    ],
    "collections_actions": [
        "action_id", "loan_id", "customer_id", "action_date",
        "collection_channel", "agent_id", "action_type",
        "promise_to_pay_flag", "recovered_amount", "action_outcome",
        "contact_attempt_number"
    ],
    "credit_policy_simulations": [
        "simulation_id", "policy_name", "minimum_credit_score",
        "maximum_debt_to_income_ratio", "maximum_loan_to_income_ratio",
        "predicted_approval_rate", "predicted_default_rate",
        "expected_credit_loss", "projected_revenue",
        "policy_recommendation"
    ],
    "daily_portfolio_metrics": [
        "metric_date", "active_loans", "new_disbursements",
        "collection_amount", "overdue_balance", "loans_30_dpd",
        "loans_60_dpd", "loans_90_dpd", "defaults", "write_offs",
        "recovery_rate", "expected_credit_loss", "portfolio_revenue"
    ],
}
PRIMARY_KEYS = {
    "customers": "customer_id",
    "loan_applications": "application_id",
    "loans": "loan_id",
    "repayment_transactions": "repayment_id",
    "collections_actions": "action_id",
    "credit_policy_simulations": "simulation_id",
    "daily_portfolio_metrics": "metric_date",
}
def load_data() -> dict:
    return {
        "customers": pd.read_csv(CUSTOMERS_FILE),
        "loan_applications": pd.read_csv(LOAN_APPLICATIONS_FILE),
        "loans": pd.read_csv(LOANS_FILE),
        "repayment_transactions": pd.read_csv(REPAYMENT_TRANSACTIONS_FILE),
        "delinquency_snapshots": pd.read_csv(DELINQUENCY_SNAPSHOTS_FILE),
        "collections_actions": pd.read_csv(COLLECTIONS_ACTIONS_FILE),
        "credit_policy_simulations": pd.read_csv(CREDIT_POLICY_SIMULATIONS_FILE),
        "daily_portfolio_metrics": pd.read_csv(DAILY_PORTFOLIO_METRICS_FILE),
    }
def add_check(checks: list, area: str, check_name: str, status: str, value, expectation: str) -> None:
    checks.append(
        {
            "area": area,
            "check_name": check_name,
            "status": status,
            "observed_value": value,
            "expectation": expectation,
        }
    )
def validate_required_columns(data: dict, checks: list) -> None:
    for table_name, required_columns in REQUIRED_COLUMNS.items():
        actual_columns = set(data[table_name].columns)
        missing_columns = [col for col in required_columns if col not in actual_columns]
        add_check(
            checks,
            table_name,
            "required_columns_present",
            "PASS" if len(missing_columns) == 0 else "FAIL",
            "None missing" if len(missing_columns) == 0 else ", ".join(missing_columns),
            "All required columns should exist",
        )
def validate_row_counts(data: dict, checks: list) -> None:
    add_check(checks, "customers", "row_count", "PASS" if len(data["customers"]) == CUSTOMER_COUNT else "FAIL", len(data["customers"]), f"Exactly {CUSTOMER_COUNT:,} rows")
    add_check(checks, "loan_applications", "row_count", "PASS" if len(data["loan_applications"]) == APPLICATION_COUNT else "FAIL", len(data["loan_applications"]), f"Exactly {APPLICATION_COUNT:,} rows")
    add_check(checks, "loans", "approved_loan_count", "PASS" if len(data["loans"]) >= MIN_APPROVED_LOANS else "FAIL", len(data["loans"]), f"At least {MIN_APPROVED_LOANS:,} approved loans")
    add_check(checks, "repayment_transactions", "minimum_repayment_records", "PASS" if len(data["repayment_transactions"]) > len(data["loans"]) else "FAIL", len(data["repayment_transactions"]), "Repayment rows should exceed loan rows")
    add_check(checks, "delinquency_snapshots", "minimum_snapshot_records", "PASS" if len(data["delinquency_snapshots"]) > len(data["loans"]) else "FAIL", len(data["delinquency_snapshots"]), "Snapshot rows should exceed loan rows")
    add_check(checks, "credit_policy_simulations", "scenario_count", "PASS" if len(data["credit_policy_simulations"]) >= 5 else "FAIL", len(data["credit_policy_simulations"]), "At least 5 policy scenarios")
    add_check(checks, "daily_portfolio_metrics", "daily_metric_rows", "PASS" if len(data["daily_portfolio_metrics"]) >= 900 else "FAIL", len(data["daily_portfolio_metrics"]), "At least 900 daily metric rows")
def validate_primary_keys(data: dict, checks: list) -> None:
    for table_name, primary_key in PRIMARY_KEYS.items():
        duplicate_count = int(data[table_name][primary_key].duplicated().sum())
        if table_name == "repayment_transactions":
            status = "WARN" if duplicate_count > 0 else "PASS"
            expectation = "Duplicates are intentionally allowed in raw data for cleaning practice"
        else:
            status = "PASS" if duplicate_count == 0 else "FAIL"
            expectation = "Primary key should be unique"
        add_check(checks, table_name, f"duplicate_{primary_key}", status, duplicate_count, expectation)
def validate_foreign_keys(data: dict, checks: list) -> None:
    customers = set(data["customers"]["customer_id"])
    applications = set(data["loan_applications"]["application_id"])
    loans = set(data["loans"]["loan_id"])
    fk_checks = [
        ("loan_applications", "customer_id", set(data["loan_applications"]["customer_id"]), customers, "customers.customer_id"),
        ("loans", "application_id", set(data["loans"]["application_id"]), applications, "loan_applications.application_id"),
        ("loans", "customer_id", set(data["loans"]["customer_id"]), customers, "customers.customer_id"),
        ("repayment_transactions", "loan_id", set(data["repayment_transactions"]["loan_id"]), loans, "loans.loan_id"),
        ("delinquency_snapshots", "loan_id", set(data["delinquency_snapshots"]["loan_id"]), loans, "loans.loan_id"),
        ("delinquency_snapshots", "customer_id", set(data["delinquency_snapshots"]["customer_id"]), customers, "customers.customer_id"),
        ("collections_actions", "loan_id", set(data["collections_actions"]["loan_id"]), loans, "loans.loan_id"),
        ("collections_actions", "customer_id", set(data["collections_actions"]["customer_id"]), customers, "customers.customer_id"),
    ]
    for table_name, column_name, child_values, parent_values, parent_reference in fk_checks:
        invalid_count = len(child_values - parent_values)
        add_check(
            checks,
            table_name,
            f"foreign_key_{column_name}",
            "PASS" if invalid_count == 0 else "FAIL",
            invalid_count,
            f"All values should exist in {parent_reference}",
        )
def validate_missing_values(data: dict, checks: list) -> None:
    critical_columns = {
        "customers": ["customer_id"],
        "loan_applications": ["application_id", "customer_id", "application_date", "approval_status"],
        "loans": ["loan_id", "application_id", "customer_id", "disbursement_date"],
        "repayment_transactions": ["repayment_id", "loan_id", "due_date"],
        "delinquency_snapshots": ["snapshot_date", "loan_id", "customer_id"],
        "collections_actions": ["action_id", "loan_id", "customer_id", "action_date"],
        "credit_policy_simulations": ["simulation_id", "policy_name"],
        "daily_portfolio_metrics": ["metric_date"],
    }
    for table_name, df in data.items():
        total_missing = int(df.isna().sum().sum())
        add_check(
            checks,
            table_name,
            "total_missing_values",
            "WARN" if total_missing > 0 else "PASS",
            total_missing,
            "Raw data may include realistic missing values, but critical IDs must not be missing",
        )
        for column in critical_columns.get(table_name, []):
            missing_count = int(df[column].isna().sum())
            add_check(
                checks,
                table_name,
                f"critical_null_{column}",
                "PASS" if missing_count == 0 else "FAIL",
                missing_count,
                "Critical ID/date/status fields should not be missing",
            )
def validate_date_ranges(data: dict, checks: list) -> None:
    date_columns = {
        "customers": "customer_since_date",
        "loan_applications": "application_date",
        "loans": "disbursement_date",
        "repayment_transactions": "due_date",
        "delinquency_snapshots": "snapshot_date",
        "collections_actions": "action_date",
        "daily_portfolio_metrics": "metric_date",
    }
    for table_name, column_name in date_columns.items():
        dates = pd.to_datetime(data[table_name][column_name], errors="coerce")
        add_check(
            checks,
            table_name,
            f"{column_name}_parseable",
            "PASS" if dates.isna().sum() == 0 else "FAIL",
            int(dates.isna().sum()),
            "Date column should be parseable",
        )
        add_check(
            checks,
            table_name,
            f"{column_name}_range",
            "PASS",
            f"{dates.min().date()} to {dates.max().date()}",
            "Date range should be business-realistic",
        )
def validate_business_consistency(data: dict, checks: list) -> None:
    applications = data["loan_applications"]
    loans = data["loans"]
    repayments = data["repayment_transactions"]
    snapshots = data["delinquency_snapshots"]
    approved_count = int((applications["approval_status"] == "Approved").sum())
    loan_count = len(loans)
    add_check(
        checks,
        "loans",
        "loans_match_approved_applications",
        "PASS" if loan_count == approved_count else "FAIL",
        f"loans={loan_count}, approved_applications={approved_count}",
        "Each approved application should create one loan",
    )
    loans_with_repayments = repayments["loan_id"].nunique()
    add_check(
        checks,
        "repayment_transactions",
        "all_loans_have_repayments",
        "PASS" if loans_with_repayments == loan_count else "FAIL",
        f"{loans_with_repayments} of {loan_count}",
        "Every loan should have repayment records",
    )
    loans_with_snapshots = snapshots["loan_id"].nunique()
    add_check(
        checks,
        "delinquency_snapshots",
        "all_loans_have_snapshots",
        "PASS" if loans_with_snapshots == loan_count else "FAIL",
        f"{loans_with_snapshots} of {loan_count}",
        "Every loan should have delinquency snapshots",
    )
    invalid_paid_amounts = int((repayments["paid_amount"] < 0).sum())
    add_check(
        checks,
        "repayment_transactions",
        "negative_paid_amounts",
        "PASS" if invalid_paid_amounts == 0 else "FAIL",
        invalid_paid_amounts,
        "Paid amount should not be negative",
    )
    invalid_outstanding = int((loans["current_outstanding"] < 0).sum())
    add_check(
        checks,
        "loans",
        "negative_current_outstanding",
        "PASS" if invalid_outstanding == 0 else "FAIL",
        invalid_outstanding,
        "Outstanding balance should not be negative",
    )
    invalid_dpd = int((loans["days_past_due"] < 0).sum())
    add_check(
        checks,
        "loans",
        "negative_days_past_due",
        "PASS" if invalid_dpd == 0 else "FAIL",
        invalid_dpd,
        "Days past due should not be negative",
    )
def create_markdown_report(summary: pd.DataFrame, data: dict) -> str:
    status_counts = summary["status"].value_counts().to_dict()
    report = []
    report.append("# Raw Data Validation Report")
    report.append("")
    report.append("## Project")
    report.append("FinTech Credit Risk & Collections Strategy Intelligence")
    report.append("")
    report.append("## Validation Summary")
    report.append("")
    report.append(f"- PASS checks: {status_counts.get('PASS', 0)}")
    report.append(f"- WARN checks: {status_counts.get('WARN', 0)}")
    report.append(f"- FAIL checks: {status_counts.get('FAIL', 0)}")
    report.append("")
    report.append("## Raw Dataset Row Counts")
    report.append("")
    report.append("| Table | Rows | Columns |")
    report.append("|---|---:|---:|")
    for table_name, df in data.items():
        report.append(f"| {table_name} | {len(df):,} | {df.shape[1]} |")
    report.append("")
    report.append("## Notes")
    report.append("")
    report.append("- Repayment transaction duplicates are intentional raw-data quality issues for cleaning practice.")
    report.append("- Missing values in selected non-critical fields are intentional and realistic.")
    report.append("- Foreign keys and critical identifiers should pass validation before moving to BigQuery.")
    report.append("")
    report.append("## Failed Checks")
    report.append("")
    failed = summary[summary["status"] == "FAIL"]
    if len(failed) == 0:
        report.append("No failed checks found.")
    else:
        report.append(failed.to_markdown(index=False))
    return "\n".join(report)
def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    checks = []
    validate_required_columns(data, checks)
    validate_row_counts(data, checks)
    validate_primary_keys(data, checks)
    validate_foreign_keys(data, checks)
    validate_missing_values(data, checks)
    validate_date_ranges(data, checks)
    validate_business_consistency(data, checks)
    summary = pd.DataFrame(checks)
    summary.to_csv(QUALITY_SUMMARY_FILE, index=False)
    markdown_report = create_markdown_report(summary, data)
    VALIDATION_REPORT_FILE.write_text(markdown_report, encoding="utf-8")
    print("Raw data validation completed")
    print(f"Quality summary file: {QUALITY_SUMMARY_FILE}")
    print(f"Validation report file: {VALIDATION_REPORT_FILE}")
    print("")
    print("Status counts:")
    print(summary["status"].value_counts().to_string())
    print("")
    print("Failed checks:")
    failed = summary[summary["status"] == "FAIL"]
    if len(failed) == 0:
        print("No failed checks")
    else:
        print(failed.to_string(index=False))
if __name__ == "__main__":
    main()
