import numpy as np
import pandas as pd
from src.config import (
    LOANS_FILE,
    REPAYMENT_TRANSACTIONS_FILE,
    DELINQUENCY_SNAPSHOTS_FILE,
    COLLECTIONS_ACTIONS_FILE,
    DAILY_PORTFOLIO_METRICS_FILE,
    START_DATE,
    END_DATE,
)
def generate_daily_portfolio_metrics() -> pd.DataFrame:
    loans = pd.read_csv(LOANS_FILE)
    repayments = pd.read_csv(REPAYMENT_TRANSACTIONS_FILE)
    snapshots = pd.read_csv(DELINQUENCY_SNAPSHOTS_FILE)
    collections = pd.read_csv(COLLECTIONS_ACTIONS_FILE)
    loans["disbursement_date"] = pd.to_datetime(loans["disbursement_date"])
    loans["closure_date"] = pd.to_datetime(loans["closure_date"], errors="coerce")
    repayments["payment_date"] = pd.to_datetime(repayments["payment_date"], errors="coerce")
    snapshots["snapshot_date"] = pd.to_datetime(snapshots["snapshot_date"])
    collections["action_date"] = pd.to_datetime(collections["action_date"], errors="coerce")
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
    metrics = pd.DataFrame({"metric_date": date_range})
    disbursements_daily = loans.groupby("disbursement_date")["principal_amount"].sum().rename("new_disbursements")
    collection_daily = collections.groupby("action_date")["recovered_amount"].sum().rename("collection_amount")
    repayment_daily = repayments.groupby("payment_date")["paid_amount"].sum().rename("repayment_amount")
    metrics = metrics.merge(disbursements_daily, left_on="metric_date", right_index=True, how="left")
    metrics = metrics.merge(collection_daily, left_on="metric_date", right_index=True, how="left")
    metrics = metrics.merge(repayment_daily, left_on="metric_date", right_index=True, how="left")
    metrics["new_disbursements"] = metrics["new_disbursements"].fillna(0)
    metrics["collection_amount"] = metrics["collection_amount"].fillna(0)
    metrics["repayment_amount"] = metrics["repayment_amount"].fillna(0)
    daily_rows = []
    for current_date in date_range:
        active_mask = (
            (loans["disbursement_date"] <= current_date)
            & (
                loans["closure_date"].isna()
                | (loans["closure_date"] > current_date)
            )
            & (loans["loan_status"] != "Written Off")
        )
        active_loans = int(active_mask.sum())
        cumulative_defaults = int(
            loans[
                (loans["default_flag"] == 1)
                & (loans["disbursement_date"] <= current_date)
            ].shape[0]
        )
        cumulative_write_offs = int(
            loans[
                (loans["write_off_flag"] == 1)
                & (loans["disbursement_date"] <= current_date)
            ].shape[0]
        )
        daily_rows.append(
            {
                "metric_date": current_date,
                "active_loans": active_loans,
                "defaults": cumulative_defaults,
                "write_offs": cumulative_write_offs,
            }
        )
    active_df = pd.DataFrame(daily_rows)
    metrics = metrics.merge(active_df, on="metric_date", how="left")
    snapshot_metrics = snapshots.groupby("snapshot_date").agg(
        overdue_balance=(
            "outstanding_balance",
            lambda x: x[snapshots.loc[x.index, "days_past_due"] > 0].sum(),
        ),
        loans_30_dpd=(
            "days_past_due",
            lambda x: int((x >= 30).sum()),
        ),
        loans_60_dpd=(
            "days_past_due",
            lambda x: int((x >= 60).sum()),
        ),
        loans_90_dpd=(
            "days_past_due",
            lambda x: int((x >= 90).sum()),
        ),
        snapshot_outstanding=("outstanding_balance", "sum"),
    ).reset_index()
    metrics = metrics.merge(
        snapshot_metrics,
        left_on="metric_date",
        right_on="snapshot_date",
        how="left",
    )
    metrics = metrics.drop(columns=["snapshot_date"])
    metrics[
        [
            "overdue_balance",
            "loans_30_dpd",
            "loans_60_dpd",
            "loans_90_dpd",
            "snapshot_outstanding",
        ]
    ] = metrics[
        [
            "overdue_balance",
            "loans_30_dpd",
            "loans_60_dpd",
            "loans_90_dpd",
            "snapshot_outstanding",
        ]
    ].ffill().fillna(0)
    metrics["portfolio_revenue"] = metrics["repayment_amount"] * 0.18
    metrics["recovery_rate"] = np.where(
        metrics["overdue_balance"] > 0,
        metrics["collection_amount"] / metrics["overdue_balance"],
        0,
    )
    metrics["recovery_rate"] = metrics["recovery_rate"].clip(lower=0, upper=1)
    metrics["expected_credit_loss"] = (
        metrics["snapshot_outstanding"] * 0.085
        + metrics["loans_30_dpd"] * 1200
        + metrics["loans_60_dpd"] * 2500
        + metrics["loans_90_dpd"] * 5000
    )
    metrics = metrics[
        [
            "metric_date",
            "active_loans",
            "new_disbursements",
            "collection_amount",
            "overdue_balance",
            "loans_30_dpd",
            "loans_60_dpd",
            "loans_90_dpd",
            "defaults",
            "write_offs",
            "recovery_rate",
            "expected_credit_loss",
            "portfolio_revenue",
        ]
    ].copy()
    metrics["metric_date"] = metrics["metric_date"].dt.date
    amount_columns = [
        "new_disbursements",
        "collection_amount",
        "overdue_balance",
        "expected_credit_loss",
        "portfolio_revenue",
    ]
    for column in amount_columns:
        metrics[column] = metrics[column].round(2)
    metrics["recovery_rate"] = metrics["recovery_rate"].round(4)
    count_columns = [
        "active_loans",
        "loans_30_dpd",
        "loans_60_dpd",
        "loans_90_dpd",
        "defaults",
        "write_offs",
    ]
    for column in count_columns:
        metrics[column] = metrics[column].astype(int)
    return metrics
def main() -> None:
    metrics = generate_daily_portfolio_metrics()
    DAILY_PORTFOLIO_METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(DAILY_PORTFOLIO_METRICS_FILE, index=False)
    print("daily_portfolio_metrics.csv generated successfully")
    print(f"Output file: {DAILY_PORTFOLIO_METRICS_FILE}")
    print(f"Rows: {len(metrics):,}")
    print(f"Columns: {metrics.shape[1]}")
    print("")
    print("Date range:")
    print(f"Min: {metrics['metric_date'].min()}")
    print(f"Max: {metrics['metric_date'].max()}")
    print("")
    print("Latest portfolio metrics:")
    print(metrics.tail(1).to_string(index=False))
if __name__ == "__main__":
    main()
