import numpy as np
import pandas as pd
from src.config import (
    CUSTOMERS_FILE,
    LOAN_APPLICATIONS_FILE,
    LOANS_FILE,
    CREDIT_POLICY_SIMULATIONS_FILE,
)
POLICY_SCENARIOS = [
    {
        "policy_name": "Very Conservative Policy",
        "minimum_credit_score": 720,
        "maximum_debt_to_income_ratio": 0.38,
        "maximum_loan_to_income_ratio": 3.0,
    },
    {
        "policy_name": "Conservative Policy",
        "minimum_credit_score": 690,
        "maximum_debt_to_income_ratio": 0.42,
        "maximum_loan_to_income_ratio": 3.8,
    },
    {
        "policy_name": "Balanced Risk-Return Policy",
        "minimum_credit_score": 650,
        "maximum_debt_to_income_ratio": 0.50,
        "maximum_loan_to_income_ratio": 5.0,
    },
    {
        "policy_name": "Current-Like Growth Policy",
        "minimum_credit_score": 620,
        "maximum_debt_to_income_ratio": 0.58,
        "maximum_loan_to_income_ratio": 6.5,
    },
    {
        "policy_name": "Growth Expansion Policy",
        "minimum_credit_score": 590,
        "maximum_debt_to_income_ratio": 0.66,
        "maximum_loan_to_income_ratio": 8.0,
    },
    {
        "policy_name": "Aggressive Growth Policy",
        "minimum_credit_score": 560,
        "maximum_debt_to_income_ratio": 0.74,
        "maximum_loan_to_income_ratio": 10.0,
    },
    {
        "policy_name": "Thin-File Inclusion Policy",
        "minimum_credit_score": 540,
        "maximum_debt_to_income_ratio": 0.60,
        "maximum_loan_to_income_ratio": 4.5,
    },
    {
        "policy_name": "High-Income Flexible Policy",
        "minimum_credit_score": 600,
        "maximum_debt_to_income_ratio": 0.70,
        "maximum_loan_to_income_ratio": 7.5,
    },
]
def risk_proxy_default_rate(row: pd.Series) -> float:
    credit_score = row["credit_score"]
    dti = row["debt_to_income_ratio"]
    lti = row["loan_to_income_ratio"]
    underwriting_score = row["underwriting_score"]
    product = row["loan_product"]
    base = 0.08
    if credit_score < 580:
        base += 0.14
    elif credit_score < 640:
        base += 0.08
    elif credit_score < 700:
        base += 0.035
    elif credit_score >= 760:
        base -= 0.025
    if dti > 0.65:
        base += 0.11
    elif dti > 0.55:
        base += 0.07
    elif dti > 0.45:
        base += 0.035
    elif dti < 0.25:
        base -= 0.02
    if lti > 8:
        base += 0.07
    elif lti > 6:
        base += 0.04
    elif lti > 4:
        base += 0.02
    if underwriting_score < 45:
        base += 0.12
    elif underwriting_score < 61:
        base += 0.06
    elif underwriting_score >= 76:
        base -= 0.025
    if product == "Business Micro-loan":
        base += 0.035
    elif product == "Consumer Durable Loan":
        base -= 0.015
    return float(max(0.01, min(base, 0.55)))
def recommend_policy(approval_rate: float, default_rate: float, ecl_ratio: float, profit_after_loss: float) -> str:
    if default_rate <= 0.09 and approval_rate >= 0.35 and profit_after_loss > 0:
        return "Recommended: strong risk-return balance"
    if default_rate <= 0.07 and approval_rate < 0.35:
        return "Safe but restrictive: consider relaxing slightly"
    if default_rate > 0.18:
        return "Not recommended: default risk too high"
    if ecl_ratio > 0.18:
        return "Not recommended: expected loss exposure too high"
    if profit_after_loss <= 0:
        return "Not recommended: weak profitability after expected losses"
    return "Monitor: acceptable but needs segment-level controls"
def generate_credit_policy_simulations() -> pd.DataFrame:
    customers = pd.read_csv(CUSTOMERS_FILE)
    applications = pd.read_csv(LOAN_APPLICATIONS_FILE)
    loans = pd.read_csv(LOANS_FILE)
    apps = applications.merge(customers, on="customer_id", how="left")
    loan_defaults = loans[
        ["application_id", "default_flag", "write_off_flag", "current_outstanding"]
    ].copy()
    apps = apps.merge(loan_defaults, on="application_id", how="left")
    apps["loan_to_income_ratio"] = apps["requested_amount"] / apps["monthly_income"].clip(lower=1)
    apps["proxy_pd"] = apps.apply(risk_proxy_default_rate, axis=1)
    apps["default_flag"] = apps["default_flag"].fillna(0)
    apps["write_off_flag"] = apps["write_off_flag"].fillna(0)
    apps["current_outstanding"] = apps["current_outstanding"].fillna(0)
    total_applications = len(apps)
    simulations = []
    for index, scenario in enumerate(POLICY_SCENARIOS, start=1):
        eligible = apps[
            (apps["credit_score"] >= scenario["minimum_credit_score"])
            & (apps["debt_to_income_ratio"] <= scenario["maximum_debt_to_income_ratio"])
            & (apps["loan_to_income_ratio"] <= scenario["maximum_loan_to_income_ratio"])
        ].copy()
        if len(eligible) == 0:
            approval_rate = 0
            default_rate = 0
            expected_credit_loss = 0
            projected_revenue = 0
            recommendation = "Not recommended: no eligible applications"
        else:
            approval_rate = len(eligible) / total_applications
            observed_defaults = eligible[eligible["approval_status"] == "Approved"]["default_flag"]
            if len(observed_defaults) >= 100:
                observed_default_rate = observed_defaults.mean()
                proxy_default_rate = eligible["proxy_pd"].mean()
                default_rate = (observed_default_rate * 0.65) + (proxy_default_rate * 0.35)
            else:
                default_rate = eligible["proxy_pd"].mean()
            average_exposure = eligible["requested_amount"].mean()
            total_exposure = eligible["requested_amount"].sum()
            lgd = 0.58
            expected_credit_loss = total_exposure * default_rate * lgd
            weighted_interest_rate = eligible["interest_rate_offered"].mean() / 100
            average_tenure_years = eligible["requested_tenure_months"].mean() / 12
            projected_revenue = total_exposure * weighted_interest_rate * average_tenure_years * 0.72
            ecl_ratio = expected_credit_loss / max(total_exposure, 1)
            profit_after_loss = projected_revenue - expected_credit_loss
            recommendation = recommend_policy(
                approval_rate=approval_rate,
                default_rate=default_rate,
                ecl_ratio=ecl_ratio,
                profit_after_loss=profit_after_loss,
            )
        simulations.append(
            {
                "simulation_id": f"SIM{index:04d}",
                "policy_name": scenario["policy_name"],
                "minimum_credit_score": scenario["minimum_credit_score"],
                "maximum_debt_to_income_ratio": scenario["maximum_debt_to_income_ratio"],
                "maximum_loan_to_income_ratio": scenario["maximum_loan_to_income_ratio"],
                "predicted_approval_rate": round(float(approval_rate), 4),
                "predicted_default_rate": round(float(default_rate), 4),
                "expected_credit_loss": round(float(expected_credit_loss), 2),
                "projected_revenue": round(float(projected_revenue), 2),
                "policy_recommendation": recommendation,
            }
        )
    return pd.DataFrame(simulations)
def main() -> None:
    simulations = generate_credit_policy_simulations()
    CREDIT_POLICY_SIMULATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    simulations.to_csv(CREDIT_POLICY_SIMULATIONS_FILE, index=False)
    print("credit_policy_simulations.csv generated successfully")
    print(f"Output file: {CREDIT_POLICY_SIMULATIONS_FILE}")
    print(f"Rows: {len(simulations):,}")
    print(f"Columns: {simulations.shape[1]}")
    print("")
    print(simulations.to_string(index=False))
if __name__ == "__main__":
    main()
