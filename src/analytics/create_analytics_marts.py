import numpy as np
import pandas as pd
from src.config import PROCESSED_DATA_DIR, PROJECT_ROOT
MARTS_DIR = PROJECT_ROOT / "data" / "marts"
MART_SUMMARY_FILE = PROJECT_ROOT / "outputs" / "reports" / "analytics_mart_summary.csv"
def bucket_income(income: float) -> str:
    if income < 25000:
        return "Low Income"
    if income < 50000:
        return "Mass Market"
    if income < 100000:
        return "Upper Mass"
    if income < 200000:
        return "Affluent"
    return "High Income"
def dpd_bucket(days_past_due: int, default_flag: int, write_off_flag: int) -> str:
    if write_off_flag == 1:
        return "Write-off"
    if default_flag == 1:
        return "Default"
    if days_past_due >= 90:
        return "90+ DPD"
    if days_past_due >= 60:
        return "61-90 DPD"
    if days_past_due >= 30:
        return "31-60 DPD"
    if days_past_due > 0:
        return "1-30 DPD"
    return "Current"
def pd_proxy(row: pd.Series) -> float:
    risk_band_pd = {
        "Low": 0.035,
        "Medium": 0.085,
        "High": 0.180,
        "Critical": 0.330,
    }
    product_multiplier = {
        "Consumer Durable Loan": 0.82,
        "Salary Advance": 0.95,
        "Personal Loan": 1.05,
        "Business Micro-loan": 1.25,
    }
    employment_multiplier = {
        "Salaried": 0.82,
        "Self-employed": 1.05,
        "Small Business Owner": 1.15,
        "Contract Worker": 1.22,
        "Gig Worker": 1.32,
    }
    base = risk_band_pd.get(row["risk_band"], 0.12)
    base *= product_multiplier.get(row["loan_product"], 1.0)
    base *= employment_multiplier.get(row["employment_type"], 1.0)
    if row["debt_to_income_ratio"] >= 0.60:
        base *= 1.25
    elif row["debt_to_income_ratio"] <= 0.25:
        base *= 0.82
    if row["credit_score"] >= 760:
        base *= 0.72
    elif row["credit_score"] < 600:
        base *= 1.28
    if row["days_past_due"] >= 90:
        base = max(base, 0.55)
    elif row["days_past_due"] >= 60:
        base = max(base, 0.38)
    elif row["days_past_due"] >= 30:
        base = max(base, 0.24)
    return round(float(max(0.01, min(base, 0.85))), 4)
def risk_priority_band(score: float) -> str:
    if score >= 80:
        return "Critical Priority"
    if score >= 60:
        return "High Priority"
    if score >= 35:
        return "Medium Priority"
    return "Low Priority"
def create_loan_risk_mart(customers, apps, loans, repayments, snapshots):
    latest_snapshots = (
        snapshots.sort_values(["loan_id", "snapshot_date"])
        .groupby("loan_id", as_index=False)
        .tail(1)
    )
    repayment_features = repayments.groupby("loan_id").agg(
        total_due_amount=("due_amount", "sum"),
        total_paid_amount=("paid_amount", "sum"),
        repayment_count=("repayment_id", "count"),
        missed_payment_count=("payment_status", lambda x: int((x == "Missed").sum())),
        partial_payment_count=("payment_status", lambda x: int((x == "Partial").sum())),
        late_payment_count=("payment_status", lambda x: int((x == "Late").sum())),
        avg_days_late=("days_late", "mean"),
        max_days_late=("days_late", "max"),
    ).reset_index()
    mart = loans.merge(
        apps,
        on=["application_id", "customer_id"],
        how="left",
        suffixes=("", "_application"),
    ).merge(
        customers,
        on="customer_id",
        how="left",
    ).merge(
        latest_snapshots[
            [
                "loan_id",
                "snapshot_date",
                "outstanding_balance",
                "delinquency_bucket",
                "roll_rate_stage",
                "collection_status",
            ]
        ],
        on="loan_id",
        how="left",
    ).merge(
        repayment_features,
        on="loan_id",
        how="left",
    )
    mart["income_band"] = mart["monthly_income"].apply(bucket_income)
    mart["loan_to_income_ratio"] = mart["principal_amount"] / mart["monthly_income"].clip(lower=1)
    mart["repayment_completion_rate"] = mart["total_paid_amount"] / mart["total_due_amount"].replace(0, np.nan)
    mart["repayment_completion_rate"] = mart["repayment_completion_rate"].fillna(0).clip(0, 1.5).round(4)
    mart["pd_score"] = mart.apply(pd_proxy, axis=1)
    mart["lgd"] = np.where(
        mart["write_off_flag"] == 1,
        0.85,
        np.where(mart["default_flag"] == 1, 0.68, np.where(mart["days_past_due"] >= 60, 0.58, 0.45)),
    )
    mart["ead"] = mart["current_outstanding"].clip(lower=0)
    mart["expected_credit_loss"] = (mart["pd_score"] * mart["lgd"] * mart["ead"]).round(2)
    mart["par30_flag"] = (mart["days_past_due"] >= 30).astype(int)
    mart["par60_flag"] = (mart["days_past_due"] >= 60).astype(int)
    mart["par90_flag"] = (mart["days_past_due"] >= 90).astype(int)
    mart["risk_priority_score"] = (
        mart["pd_score"] * 45
        + mart["par30_flag"] * 12
        + mart["par60_flag"] * 12
        + mart["par90_flag"] * 16
        + (mart["current_outstanding"] / mart["current_outstanding"].max()) * 15
    ).round(2)
    mart["risk_priority_band"] = mart["risk_priority_score"].apply(risk_priority_band)
    final_cols = [
        "loan_id", "application_id", "customer_id", "state", "city",
        "gender", "employment_type", "occupation_category", "income_band",
        "monthly_income", "credit_score", "debt_to_income_ratio",
        "acquisition_channel", "loan_product", "purpose_category", "risk_band",
        "underwriting_score", "disbursement_date", "principal_amount",
        "interest_rate", "tenure_months", "emi_amount", "loan_status",
        "current_outstanding", "days_past_due", "delinquency_bucket",
        "default_flag", "write_off_flag", "total_due_amount",
        "total_paid_amount", "repayment_completion_rate",
        "missed_payment_count", "partial_payment_count", "late_payment_count",
        "avg_days_late", "max_days_late", "pd_score", "lgd", "ead",
        "expected_credit_loss", "par30_flag", "par60_flag", "par90_flag",
        "risk_priority_score", "risk_priority_band"
    ]
    return mart[final_cols].copy()
def create_collections_work_queue(loan_risk_mart, collections):
    collection_features = collections.groupby("loan_id").agg(
        total_contact_attempts=("action_id", "count"),
        total_recovered_amount=("recovered_amount", "sum"),
        promise_to_pay_count=("promise_to_pay_flag", "sum"),
        last_action_date=("action_date", "max"),
        last_contact_attempt_number=("contact_attempt_number", "max"),
    ).reset_index()
    queue = loan_risk_mart.merge(collection_features, on="loan_id", how="left")
    fill_cols = ["total_contact_attempts", "total_recovered_amount", "promise_to_pay_count", "last_contact_attempt_number"]
    for col in fill_cols:
        queue[col] = queue[col].fillna(0)
    queue["last_action_date"] = queue["last_action_date"].fillna("No Prior Contact")
    queue = queue[
        (queue["loan_status"].isin(["Active", "Defaulted"]))
        & (queue["days_past_due"] > 0)
        & (queue["write_off_flag"] == 0)
    ].copy()
    queue["expected_recoverable_value"] = (
        queue["current_outstanding"]
        * (1 - queue["lgd"])
        * (1 + queue["promise_to_pay_count"].clip(0, 3) * 0.06)
    ).round(2)
    queue["collections_priority_score"] = (
        queue["risk_priority_score"] * 0.45
        + queue["days_past_due"].clip(0, 180) / 180 * 25
        + queue["current_outstanding"] / queue["current_outstanding"].max() * 20
        - queue["total_contact_attempts"].clip(0, 10) * 1.2
        + queue["promise_to_pay_count"].clip(0, 5) * 2
    ).round(2)
    def next_action(row):
        if row["days_past_due"] <= 30:
            return "Digital reminder + payment link"
        if row["days_past_due"] <= 60:
            return "Priority phone call"
        if row["days_past_due"] <= 90:
            return "Escalated call + field follow-up"
        if row["default_flag"] == 1:
            return "Settlement offer / legal review"
        return "Senior collections review"
    queue["recommended_next_action"] = queue.apply(next_action, axis=1)
    queue = queue.sort_values("collections_priority_score", ascending=False)
    return queue
def create_roll_rate_mart(snapshots):
    s = snapshots.copy()
    s["snapshot_date"] = pd.to_datetime(s["snapshot_date"])
    s = s.sort_values(["loan_id", "snapshot_date"])
    s["previous_bucket"] = s.groupby("loan_id")["delinquency_bucket"].shift(1)
    s["previous_snapshot_date"] = s.groupby("loan_id")["snapshot_date"].shift(1)
    transitions = s.dropna(subset=["previous_bucket"]).copy()
    transitions["snapshot_month"] = transitions["snapshot_date"].dt.to_period("M").astype(str)
    roll = transitions.groupby(
        ["snapshot_month", "previous_bucket", "delinquency_bucket"]
    ).agg(
        transition_count=("loan_id", "nunique"),
        outstanding_balance=("outstanding_balance", "sum"),
    ).reset_index()
    previous_totals = roll.groupby(["snapshot_month", "previous_bucket"])["transition_count"].transform("sum")
    roll["roll_rate"] = (roll["transition_count"] / previous_totals).round(4)
    return roll
def create_vintage_mart(loans, snapshots):
    base = snapshots.merge(
        loans[["loan_id", "disbursement_date", "principal_amount"]],
        on="loan_id",
        how="left",
    )
    base["snapshot_date"] = pd.to_datetime(base["snapshot_date"])
    base["disbursement_date"] = pd.to_datetime(base["disbursement_date"])
    base["origination_month"] = base["disbursement_date"].dt.to_period("M").astype(str)
    base["months_on_book"] = (
        (base["snapshot_date"].dt.year - base["disbursement_date"].dt.year) * 12
        + (base["snapshot_date"].dt.month - base["disbursement_date"].dt.month)
    )
    base = base[base["months_on_book"] >= 0].copy()
    base["dpd30_flag"] = (base["days_past_due"] >= 30).astype(int)
    base["dpd60_flag"] = (base["days_past_due"] >= 60).astype(int)
    base["dpd90_flag"] = (base["days_past_due"] >= 90).astype(int)
    vintage = base.groupby(["origination_month", "months_on_book"]).agg(
        loans_observed=("loan_id", "nunique"),
        outstanding_balance=("outstanding_balance", "sum"),
        dpd30_loans=("dpd30_flag", "sum"),
        dpd60_loans=("dpd60_flag", "sum"),
        dpd90_loans=("dpd90_flag", "sum"),
    ).reset_index()
    vintage["dpd30_rate"] = (vintage["dpd30_loans"] / vintage["loans_observed"]).round(4)
    vintage["dpd60_rate"] = (vintage["dpd60_loans"] / vintage["loans_observed"]).round(4)
    vintage["dpd90_rate"] = (vintage["dpd90_loans"] / vintage["loans_observed"]).round(4)
    return vintage
def create_segment_performance_mart(loan_risk_mart):
    dimensions = [
        "loan_product",
        "state",
        "employment_type",
        "risk_band",
        "income_band",
        "acquisition_channel",
    ]
    rows = []
    for dim in dimensions:
        grouped = loan_risk_mart.groupby(dim).agg(
            loans=("loan_id", "nunique"),
            total_principal=("principal_amount", "sum"),
            outstanding_balance=("current_outstanding", "sum"),
            avg_interest_rate=("interest_rate", "mean"),
            default_rate=("default_flag", "mean"),
            write_off_rate=("write_off_flag", "mean"),
            par30_rate=("par30_flag", "mean"),
            par60_rate=("par60_flag", "mean"),
            par90_rate=("par90_flag", "mean"),
            expected_credit_loss=("expected_credit_loss", "sum"),
            avg_pd_score=("pd_score", "mean"),
        ).reset_index()
        grouped = grouped.rename(columns={dim: "segment_value"})
        grouped["segment_type"] = dim
        rows.append(grouped)
    segment = pd.concat(rows, ignore_index=True)
    segment["avg_interest_rate"] = segment["avg_interest_rate"].round(2)
    rate_cols = ["default_rate", "write_off_rate", "par30_rate", "par60_rate", "par90_rate", "avg_pd_score"]
    for col in rate_cols:
        segment[col] = segment[col].round(4)
    amount_cols = ["total_principal", "outstanding_balance", "expected_credit_loss"]
    for col in amount_cols:
        segment[col] = segment[col].round(2)
    return segment[
        [
            "segment_type", "segment_value", "loans", "total_principal",
            "outstanding_balance", "avg_interest_rate", "default_rate",
            "write_off_rate", "par30_rate", "par60_rate", "par90_rate",
            "expected_credit_loss", "avg_pd_score",
        ]
    ]
def main():
    MARTS_DIR.mkdir(parents=True, exist_ok=True)
    customers = pd.read_csv(PROCESSED_DATA_DIR / "customers_clean.csv")
    apps = pd.read_csv(PROCESSED_DATA_DIR / "loan_applications_clean.csv")
    loans = pd.read_csv(PROCESSED_DATA_DIR / "loans_clean.csv")
    repayments = pd.read_csv(PROCESSED_DATA_DIR / "repayment_transactions_clean.csv")
    snapshots = pd.read_csv(PROCESSED_DATA_DIR / "delinquency_snapshots_clean.csv")
    collections = pd.read_csv(PROCESSED_DATA_DIR / "collections_actions_clean.csv")
    loan_risk_mart = create_loan_risk_mart(customers, apps, loans, repayments, snapshots)
    collections_work_queue = create_collections_work_queue(loan_risk_mart, collections)
    roll_rate_mart = create_roll_rate_mart(snapshots)
    vintage_mart = create_vintage_mart(loans, snapshots)
    segment_performance_mart = create_segment_performance_mart(loan_risk_mart)
    outputs = {
        "mart_loan_risk_base.csv": loan_risk_mart,
        "mart_collections_work_queue.csv": collections_work_queue,
        "mart_roll_rate_monthly.csv": roll_rate_mart,
        "mart_vintage_analysis.csv": vintage_mart,
        "mart_segment_performance.csv": segment_performance_mart,
    }
    summary_rows = []
    for file_name, df in outputs.items():
        df.to_csv(MARTS_DIR / file_name, index=False)
        summary_rows.append(
            {
                "mart_file": file_name,
                "rows": len(df),
                "columns": df.shape[1],
                "missing_values": int(df.isna().sum().sum()),
            }
        )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(MART_SUMMARY_FILE, index=False)
    print("Analytics marts created successfully")
    print(f"Marts folder: {MARTS_DIR}")
    print("")
    print(summary.to_string(index=False))
if __name__ == "__main__":
    main()
