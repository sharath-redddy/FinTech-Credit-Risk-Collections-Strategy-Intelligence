import numpy as np
import pandas as pd
from src.config import PROJECT_ROOT, PROCESSED_DATA_DIR
MARTS_DIR = PROJECT_ROOT / "data" / "marts"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
LOAN_RISK_FILE = MARTS_DIR / "mart_loan_risk_base.csv"
MODEL_PREDICTIONS_FILE = MARTS_DIR / "mart_default_risk_predictions.csv"
COLLECTIONS_QUEUE_FILE = MARTS_DIR / "mart_collections_work_queue.csv"
DAILY_METRICS_FILE = PROCESSED_DATA_DIR / "daily_portfolio_metrics_clean.csv"
CREDIT_RISK_STRATEGY_FILE = MARTS_DIR / "mart_credit_risk_strategy.csv"
EXECUTIVE_KPIS_FILE = MARTS_DIR / "mart_executive_kpis.csv"
RISK_ALERTS_FILE = MARTS_DIR / "mart_risk_alerts.csv"
SUMMARY_FILE = REPORTS_DIR / "credit_risk_strategy_mart_summary.csv"
def assign_loss_severity(ecl: float) -> str:
    if ecl >= 100000:
        return "Severe Loss Exposure"
    if ecl >= 40000:
        return "High Loss Exposure"
    if ecl >= 10000:
        return "Moderate Loss Exposure"
    return "Low Loss Exposure"
def assign_strategy_action(row: pd.Series) -> str:
    if row["model_risk_band"] == "Critical" and row["days_past_due"] >= 90:
        return "Settlement offer / legal review"
    if row["model_risk_band"] == "Critical" and row["days_past_due"] >= 60:
        return "Escalated collections follow-up"
    if row["model_risk_band"] == "High" and row["days_past_due"] >= 30:
        return "Priority phone call"
    if row["model_risk_band"] in ["High", "Critical"] and row["days_past_due"] == 0:
        return "Early warning monitoring"
    if row["days_past_due"] > 0:
        return "Digital reminder"
    return "No immediate action"
def create_credit_risk_strategy_mart() -> pd.DataFrame:
    loan_risk = pd.read_csv(LOAN_RISK_FILE)
    predictions = pd.read_csv(MODEL_PREDICTIONS_FILE)
    pred_cols = [
        "loan_id",
        "predicted_default_probability",
        "model_risk_band",
        "loss_given_default",
        "exposure_at_default",
        "model_expected_credit_loss",
    ]
    mart = loan_risk.merge(
        predictions[pred_cols],
        on="loan_id",
        how="left",
    )
    mart["final_expected_credit_loss"] = mart["model_expected_credit_loss"].fillna(mart["expected_credit_loss"]).round(2)
    mart["loss_severity_band"] = mart["final_expected_credit_loss"].apply(assign_loss_severity)
    mart["recommended_strategy_action"] = mart.apply(assign_strategy_action, axis=1)
    mart["portfolio_at_risk_flag"] = np.where(mart["days_past_due"] >= 30, 1, 0)
    mart["high_value_risk_flag"] = np.where(
        (mart["model_risk_band"].isin(["High", "Critical"]))
        & (mart["current_outstanding"] >= mart["current_outstanding"].quantile(0.75)),
        1,
        0,
    )
    mart["risk_rank"] = mart["final_expected_credit_loss"].rank(method="first", ascending=False).astype(int)
    mart = mart.sort_values("risk_rank")
    return mart
def create_executive_kpis(strategy_mart: pd.DataFrame) -> pd.DataFrame:
    daily_metrics = pd.read_csv(DAILY_METRICS_FILE)
    latest = daily_metrics.sort_values("metric_date").tail(1).iloc[0]
    active = strategy_mart[strategy_mart["loan_status"].isin(["Active", "Defaulted"])].copy()
    total_loans = len(strategy_mart)
    active_loans = len(active)
    total_outstanding = active["current_outstanding"].sum()
    total_ecl = active["final_expected_credit_loss"].sum()
    default_rate = strategy_mart["default_flag"].mean()
    write_off_rate = strategy_mart["write_off_flag"].mean()
    par30_rate = active["par30_flag"].mean()
    par60_rate = active["par60_flag"].mean()
    par90_rate = active["par90_flag"].mean()
    critical_risk_loans = int((active["model_risk_band"] == "Critical").sum())
    high_value_risk_loans = int(active["high_value_risk_flag"].sum())
    executive_recommendation = (
        "Tighten monitoring on Critical and High risk loans, prioritize high-ECL collections, and use Balanced Risk-Return Policy for new originations."
    )
    kpis = pd.DataFrame(
        [
            {
                "metric_date": latest["metric_date"],
                "total_loans": total_loans,
                "active_loans": active_loans,
                "total_portfolio_outstanding": round(total_outstanding, 2),
                "default_rate": round(default_rate, 4),
                "write_off_rate": round(write_off_rate, 4),
                "par30_rate": round(par30_rate, 4),
                "par60_rate": round(par60_rate, 4),
                "par90_rate": round(par90_rate, 4),
                "expected_credit_loss": round(total_ecl, 2),
                "latest_collection_amount": round(float(latest["collection_amount"]), 2),
                "latest_recovery_rate": round(float(latest["recovery_rate"]), 4),
                "critical_risk_loans": critical_risk_loans,
                "high_value_risk_loans": high_value_risk_loans,
                "executive_recommendation": executive_recommendation,
            }
        ]
    )
    return kpis
def create_risk_alerts(strategy_mart: pd.DataFrame) -> pd.DataFrame:
    active = strategy_mart[strategy_mart["loan_status"].isin(["Active", "Defaulted"])].copy()
    alerts = []
    state_alerts = active.groupby("state").agg(
        active_loans=("loan_id", "nunique"),
        outstanding_balance=("current_outstanding", "sum"),
        ecl=("final_expected_credit_loss", "sum"),
        par30_rate=("par30_flag", "mean"),
        default_rate=("default_flag", "mean"),
    ).reset_index()
    top_state = state_alerts.sort_values("ecl", ascending=False).head(1).iloc[0]
    alerts.append(
        {
            "alert_id": "ALERT001",
            "alert_type": "Regional ECL Concentration",
            "severity": "High",
            "alert_message": f"{top_state['state']} has the highest expected credit loss exposure.",
            "segment_type": "state",
            "segment_value": top_state["state"],
            "loans_impacted": int(top_state["active_loans"]),
            "exposure_amount": round(float(top_state["outstanding_balance"]), 2),
            "expected_credit_loss": round(float(top_state["ecl"]), 2),
            "recommended_action": "Review underwriting and collections strategy for this state.",
        }
    )
    product_alerts = active.groupby("loan_product").agg(
        active_loans=("loan_id", "nunique"),
        outstanding_balance=("current_outstanding", "sum"),
        ecl=("final_expected_credit_loss", "sum"),
        par30_rate=("par30_flag", "mean"),
        default_rate=("default_flag", "mean"),
    ).reset_index()
    top_product = product_alerts.sort_values("par30_rate", ascending=False).head(1).iloc[0]
    alerts.append(
        {
            "alert_id": "ALERT002",
            "alert_type": "Product Delinquency Risk",
            "severity": "Medium",
            "alert_message": f"{top_product['loan_product']} has the highest PAR30 rate.",
            "segment_type": "loan_product",
            "segment_value": top_product["loan_product"],
            "loans_impacted": int(top_product["active_loans"]),
            "exposure_amount": round(float(top_product["outstanding_balance"]), 2),
            "expected_credit_loss": round(float(top_product["ecl"]), 2),
            "recommended_action": "Monitor early delinquency and adjust product-level approval controls.",
        }
    )
    critical = active[active["model_risk_band"] == "Critical"]
    alerts.append(
        {
            "alert_id": "ALERT003",
            "alert_type": "Critical Risk Loan Pool",
            "severity": "Critical",
            "alert_message": "Critical model-risk loans require immediate monitoring and collections prioritization.",
            "segment_type": "model_risk_band",
            "segment_value": "Critical",
            "loans_impacted": int(len(critical)),
            "exposure_amount": round(float(critical["current_outstanding"].sum()), 2),
            "expected_credit_loss": round(float(critical["final_expected_credit_loss"].sum()), 2),
            "recommended_action": "Prioritize top expected-loss loans in the collections work queue.",
        }
    )
    high_value = active[active["high_value_risk_flag"] == 1]
    alerts.append(
        {
            "alert_id": "ALERT004",
            "alert_type": "High-Value Risk Exposure",
            "severity": "High",
            "alert_message": "High-value risky loans create concentrated loss exposure.",
            "segment_type": "high_value_risk_flag",
            "segment_value": "High Value Risk",
            "loans_impacted": int(len(high_value)),
            "exposure_amount": round(float(high_value["current_outstanding"].sum()), 2),
            "expected_credit_loss": round(float(high_value["final_expected_credit_loss"].sum()), 2),
            "recommended_action": "Create a senior collections queue for high-balance high-risk loans.",
        }
    )
    return pd.DataFrame(alerts)
def main() -> None:
    MARTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    strategy_mart = create_credit_risk_strategy_mart()
    executive_kpis = create_executive_kpis(strategy_mart)
    risk_alerts = create_risk_alerts(strategy_mart)
    strategy_mart.to_csv(CREDIT_RISK_STRATEGY_FILE, index=False)
    executive_kpis.to_csv(EXECUTIVE_KPIS_FILE, index=False)
    risk_alerts.to_csv(RISK_ALERTS_FILE, index=False)
    summary = pd.DataFrame(
        [
            {
                "file_name": "mart_credit_risk_strategy.csv",
                "rows": len(strategy_mart),
                "columns": strategy_mart.shape[1],
                "missing_values": int(strategy_mart.isna().sum().sum()),
            },
            {
                "file_name": "mart_executive_kpis.csv",
                "rows": len(executive_kpis),
                "columns": executive_kpis.shape[1],
                "missing_values": int(executive_kpis.isna().sum().sum()),
            },
            {
                "file_name": "mart_risk_alerts.csv",
                "rows": len(risk_alerts),
                "columns": risk_alerts.shape[1],
                "missing_values": int(risk_alerts.isna().sum().sum()),
            },
        ]
    )
    summary.to_csv(SUMMARY_FILE, index=False)
    print("Credit risk strategy marts created successfully")
    print("")
    print(summary.to_string(index=False))
    print("")
    print("Executive KPI preview:")
    print(executive_kpis.to_string(index=False))
    print("")
    print("Risk alerts:")
    print(risk_alerts[["alert_id", "alert_type", "severity", "segment_value", "recommended_action"]].to_string(index=False))
if __name__ == "__main__":
    main()
