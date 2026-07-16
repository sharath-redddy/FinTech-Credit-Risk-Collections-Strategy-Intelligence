import random
import numpy as np
import pandas as pd
from src.config import (
    LOANS_FILE,
    LOAN_APPLICATIONS_FILE,
    CUSTOMERS_FILE,
    DELINQUENCY_SNAPSHOTS_FILE,
    RANDOM_SEED,
    END_DATE,
)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
def get_bucket(days_past_due: int, default_flag: int, write_off_flag: int) -> str:
    if write_off_flag == 1:
        return "Write-off"
    if default_flag == 1:
        return "Default"
    if days_past_due >= 91:
        return "90+ DPD"
    if days_past_due >= 61:
        return "61-90 DPD"
    if days_past_due >= 31:
        return "31-60 DPD"
    if days_past_due >= 1:
        return "1-30 DPD"
    return "Current"
def get_roll_stage(previous_bucket: str, current_bucket: str) -> str:
    if previous_bucket is None:
        return "Opening Snapshot"
    if previous_bucket == current_bucket:
        return f"Stayed {current_bucket}"
    bucket_order = {
        "Current": 0,
        "1-30 DPD": 1,
        "31-60 DPD": 2,
        "61-90 DPD": 3,
        "90+ DPD": 4,
        "Default": 5,
        "Write-off": 6,
    }
    previous_rank = bucket_order.get(previous_bucket, 0)
    current_rank = bucket_order.get(current_bucket, 0)
    if current_rank > previous_rank:
        return f"Rolled Forward: {previous_bucket} to {current_bucket}"
    return f"Cured: {previous_bucket} to {current_bucket}"
def get_collection_status(bucket: str) -> str:
    if bucket == "Current":
        return "No Collection Required"
    if bucket == "1-30 DPD":
        return random.choices(
            ["Soft Reminder", "Digital Reminder", "Promise Tracking"],
            weights=[0.45, 0.40, 0.15],
            k=1,
        )[0]
    if bucket == "31-60 DPD":
        return random.choices(
            ["Tele Calling", "Promise Tracking", "Escalated Calling"],
            weights=[0.45, 0.25, 0.30],
            k=1,
        )[0]
    if bucket == "61-90 DPD":
        return random.choices(
            ["Escalated Calling", "Field Follow-up", "Settlement Review"],
            weights=[0.40, 0.35, 0.25],
            k=1,
        )[0]
    if bucket == "90+ DPD":
        return random.choices(
            ["Settlement Review", "Legal Notice", "Field Follow-up"],
            weights=[0.42, 0.28, 0.30],
            k=1,
        )[0]
    if bucket == "Default":
        return random.choices(
            ["Legal Review", "Settlement Offer", "Recovery Agency"],
            weights=[0.35, 0.38, 0.27],
            k=1,
        )[0]
    return "Write-off Monitoring"
def base_dpd_path(final_dpd: int, months_count: int, default_flag: int, write_off_flag: int) -> list[int]:
    if months_count <= 1:
        return [final_dpd]
    if write_off_flag == 1:
        start_dpd = random.choice([0, 0, 5, 15, 30])
        end_dpd = max(final_dpd, random.randint(150, 330))
        path = np.linspace(start_dpd, end_dpd, months_count)
    elif default_flag == 1:
        start_dpd = random.choice([0, 0, 10, 25])
        end_dpd = max(final_dpd, random.randint(95, 210))
        path = np.linspace(start_dpd, end_dpd, months_count)
    else:
        if final_dpd == 0:
            path = np.random.choice([0, 0, 0, 0, 5, 10, 15], size=months_count, replace=True)
            path[-1] = 0
        else:
            start_dpd = random.choice([0, 0, 5, 10])
            path = np.linspace(start_dpd, final_dpd, months_count)
    noise = np.random.normal(0, 8, months_count)
    dpd_values = np.maximum(0, np.round(path + noise)).astype(int)
    if default_flag == 1:
        dpd_values[-1] = max(final_dpd, 90)
    if write_off_flag == 1:
        dpd_values[-1] = max(final_dpd, 150)
    return dpd_values.tolist()
def generate_snapshots() -> pd.DataFrame:
    if not LOANS_FILE.exists():
        raise FileNotFoundError(f"Missing loans file: {LOANS_FILE}")
    loans = pd.read_csv(LOANS_FILE)
    apps = pd.read_csv(LOAN_APPLICATIONS_FILE)
    customers = pd.read_csv(CUSTOMERS_FILE)
    app_cols = ["application_id", "loan_product", "risk_band"]
    cust_cols = ["customer_id", "state", "employment_type"]
    loans = loans.merge(apps[app_cols], on="application_id", how="left")
    loans = loans.merge(customers[cust_cols], on="customer_id", how="left")
    portfolio_end = pd.to_datetime(END_DATE)
    snapshot_rows = []
    for _, loan in loans.iterrows():
        loan_id = loan["loan_id"]
        customer_id = loan["customer_id"]
        state = loan["state"]
        product = loan["loan_product"]
        disbursement_date = pd.to_datetime(loan["disbursement_date"])
        closure_date = pd.to_datetime(loan["closure_date"]) if pd.notna(loan["closure_date"]) else portfolio_end
        final_date = min(closure_date, portfolio_end)
        snapshot_dates = pd.date_range(
            start=disbursement_date,
            end=final_date,
            freq="ME",
        )
        if len(snapshot_dates) == 0:
            snapshot_dates = pd.DatetimeIndex([final_date])
        months_count = len(snapshot_dates)
        principal = float(loan["principal_amount"])
        final_outstanding = float(loan["current_outstanding"])
        final_dpd = int(loan["days_past_due"])
        default_flag_final = int(loan["default_flag"])
        write_off_flag_final = int(loan["write_off_flag"])
        dpd_path = base_dpd_path(
            final_dpd=final_dpd,
            months_count=months_count,
            default_flag=default_flag_final,
            write_off_flag=write_off_flag_final,
        )
        outstanding_path = np.linspace(
            principal,
            max(final_outstanding, 0),
            months_count,
        )
        previous_bucket = None
        for idx, snapshot_date in enumerate(snapshot_dates):
            days_past_due = int(dpd_path[idx])
            outstanding_balance = float(max(0, outstanding_path[idx] + np.random.normal(0, principal * 0.015)))
            # Intentional portfolio anomaly: Uttar Pradesh delinquency spike in Oct-Dec 2025.
            if state == "Uttar Pradesh" and snapshot_date >= pd.Timestamp("2025-10-31") and snapshot_date <= pd.Timestamp("2025-12-31"):
                if product in ["Personal Loan", "Business Micro-loan"]:
                    days_past_due = min(days_past_due + random.randint(20, 55), 160)
                    outstanding_balance = outstanding_balance * np.random.uniform(1.03, 1.12)
            default_flag = 1 if days_past_due >= 90 or default_flag_final == 1 and idx == months_count - 1 else 0
            write_off_flag = 1 if write_off_flag_final == 1 and idx == months_count - 1 else 0
            bucket = get_bucket(days_past_due, default_flag, write_off_flag)
            roll_stage = get_roll_stage(previous_bucket, bucket)
            collection_status = get_collection_status(bucket)
            snapshot_rows.append(
                {
                    "snapshot_date": snapshot_date.date(),
                    "loan_id": loan_id,
                    "customer_id": customer_id,
                    "outstanding_balance": round(outstanding_balance, 2),
                    "days_past_due": days_past_due,
                    "delinquency_bucket": bucket,
                    "roll_rate_stage": roll_stage,
                    "collection_status": collection_status,
                    "default_flag": int(default_flag),
                    "write_off_flag": int(write_off_flag),
                }
            )
            previous_bucket = bucket
    snapshots = pd.DataFrame(snapshot_rows)
    return snapshots
def main() -> None:
    snapshots = generate_snapshots()
    DELINQUENCY_SNAPSHOTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    snapshots.to_csv(DELINQUENCY_SNAPSHOTS_FILE, index=False)
    print("delinquency_snapshots.csv generated successfully")
    print(f"Output file: {DELINQUENCY_SNAPSHOTS_FILE}")
    print(f"Rows: {len(snapshots):,}")
    print(f"Columns: {snapshots.shape[1]}")
    print("")
    print("Snapshot date range:")
    print(f"Min: {snapshots['snapshot_date'].min()}")
    print(f"Max: {snapshots['snapshot_date'].max()}")
    print("")
    print("Delinquency bucket distribution:")
    print(snapshots["delinquency_bucket"].value_counts().to_string())
    print("")
    print("Sample records:")
    print(snapshots.head(5).to_string(index=False))
if __name__ == "__main__":
    main()
