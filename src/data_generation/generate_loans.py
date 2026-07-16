import random
from datetime import timedelta
import numpy as np
import pandas as pd
from src.config import (
    LOAN_APPLICATIONS_FILE,
    LOANS_FILE,
    CUSTOMERS_FILE,
    RANDOM_SEED,
    END_DATE,
)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
RISK_DEFAULT_BASE = {
    "Low": 0.025,
    "Medium": 0.065,
    "High": 0.145,
    "Critical": 0.285,
}
RISK_WRITE_OFF_BASE = {
    "Low": 0.004,
    "Medium": 0.014,
    "High": 0.045,
    "Critical": 0.105,
}
EMPLOYMENT_RISK_MULTIPLIER = {
    "Salaried": 0.80,
    "Self-employed": 1.05,
    "Small Business Owner": 1.15,
    "Contract Worker": 1.25,
    "Gig Worker": 1.35,
}
PRODUCT_RISK_MULTIPLIER = {
    "Consumer Durable Loan": 0.80,
    "Salary Advance": 0.95,
    "Personal Loan": 1.05,
    "Business Micro-loan": 1.25,
}
STATE_STRESS_MULTIPLIER = {
    "Karnataka": 0.90,
    "Telangana": 0.95,
    "Maharashtra": 0.95,
    "Tamil Nadu": 0.95,
    "Delhi": 1.00,
    "Gujarat": 1.00,
    "Kerala": 1.00,
    "Andhra Pradesh": 1.05,
    "West Bengal": 1.10,
    "Rajasthan": 1.12,
    "Madhya Pradesh": 1.18,
    "Uttar Pradesh": 1.25,
}
def calculate_emi(principal: float, annual_interest_rate: float, tenure_months: int) -> float:
    monthly_rate = annual_interest_rate / 100 / 12
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (
            ((1 + monthly_rate) ** tenure_months) - 1
        )
    return round(float(emi), 2)
def month_difference(start_date: pd.Timestamp, end_date: pd.Timestamp) -> int:
    return max(
        0,
        (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month),
    )
def estimate_remaining_balance(principal: float, annual_interest_rate: float, tenure_months: int, months_paid: int) -> float:
    monthly_rate = annual_interest_rate / 100 / 12
    months_paid = max(0, min(months_paid, tenure_months))
    if months_paid >= tenure_months:
        return 0.0
    if monthly_rate == 0:
        remaining = principal * (1 - months_paid / tenure_months)
    else:
        emi = calculate_emi(principal, annual_interest_rate, tenure_months)
        remaining = principal * ((1 + monthly_rate) ** months_paid) - (
            emi * (((1 + monthly_rate) ** months_paid - 1) / monthly_rate)
        )
    return round(float(max(0, remaining)), 2)
def assign_dpd_for_active_loan(risk_band: str, default_probability: float) -> int:
    random_value = np.random.random()
    if risk_band == "Low":
        bucket_probabilities = [0.82, 0.13, 0.04, 0.01]
    elif risk_band == "Medium":
        bucket_probabilities = [0.68, 0.20, 0.09, 0.03]
    elif risk_band == "High":
        bucket_probabilities = [0.48, 0.27, 0.16, 0.09]
    else:
        bucket_probabilities = [0.32, 0.27, 0.21, 0.20]
    bucket = random.choices(
        ["Current", "1-30", "31-60", "61-89"],
        weights=bucket_probabilities,
        k=1,
    )[0]
    if bucket == "Current":
        return 0
    if bucket == "1-30":
        return random.randint(1, 30)
    if bucket == "31-60":
        return random.randint(31, 60)
    # Higher probability loans are more likely to be close to default.
    if default_probability > 0.25:
        return random.randint(70, 89)
    return random.randint(61, 89)
def calculate_default_probability(application: pd.Series, customer: pd.Series) -> float:
    risk_band = application["risk_band"]
    employment_type = customer["employment_type"]
    loan_product = application["loan_product"]
    state = customer["state"]
    credit_score = float(customer["credit_score"])
    dti = float(customer["debt_to_income_ratio"])
    monthly_income = float(customer["monthly_income"])
    requested_amount = float(application["approved_amount"])
    tenure = int(application["requested_tenure_months"])
    loan_to_income_ratio = requested_amount / max(monthly_income, 1)
    probability = RISK_DEFAULT_BASE.get(risk_band, 0.10)
    probability *= EMPLOYMENT_RISK_MULTIPLIER.get(employment_type, 1.0)
    probability *= PRODUCT_RISK_MULTIPLIER.get(loan_product, 1.0)
    probability *= STATE_STRESS_MULTIPLIER.get(state, 1.0)
    if credit_score < 600:
        probability *= 1.25
    elif credit_score >= 750:
        probability *= 0.72
    if dti >= 0.55:
        probability *= 1.25
    elif dti <= 0.25:
        probability *= 0.82
    if loan_to_income_ratio >= 5:
        probability *= 1.20
    if tenure >= 24:
        probability *= 1.12
    return float(max(0.005, min(probability, 0.65)))
def generate_loans() -> pd.DataFrame:
    if not LOAN_APPLICATIONS_FILE.exists():
        raise FileNotFoundError(
            f"Missing loan applications file: {LOAN_APPLICATIONS_FILE}. Run Step 9 first."
        )
    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Missing customers file: {CUSTOMERS_FILE}. Run Step 8 first."
        )
    applications_df = pd.read_csv(LOAN_APPLICATIONS_FILE)
    customers_df = pd.read_csv(CUSTOMERS_FILE)
    approved_df = applications_df[
        applications_df["approval_status"] == "Approved"
    ].copy()
    approved_df = approved_df.dropna(subset=["approved_amount", "approval_date"])
    customers_lookup = customers_df.set_index("customer_id")
    portfolio_end_date = pd.to_datetime(END_DATE)
    loans = []
    for i, (_, application) in enumerate(approved_df.iterrows(), start=1):
        loan_id = f"LOAN{i:08d}"
        customer = customers_lookup.loc[application["customer_id"]]
        approval_date = pd.to_datetime(application["approval_date"])
        disbursement_lag_days = random.choices(
            [0, 1, 2, 3, 4, 5],
            weights=[0.25, 0.34, 0.22, 0.11, 0.05, 0.03],
            k=1,
        )[0]
        disbursement_date = approval_date + timedelta(days=disbursement_lag_days)
        if disbursement_date > portfolio_end_date:
            disbursement_date = approval_date
        principal_amount = float(application["approved_amount"])
        interest_rate = float(application["interest_rate_offered"])
        tenure_months = int(application["requested_tenure_months"])
        emi_amount = calculate_emi(principal_amount, interest_rate, tenure_months)
        months_elapsed = month_difference(disbursement_date, portfolio_end_date)
        months_paid_estimate = min(months_elapsed, tenure_months)
        default_probability = calculate_default_probability(application, customer)
        write_off_probability = RISK_WRITE_OFF_BASE.get(application["risk_band"], 0.02)
        write_off_probability *= EMPLOYMENT_RISK_MULTIPLIER.get(customer["employment_type"], 1.0)
        write_off_probability *= PRODUCT_RISK_MULTIPLIER.get(application["loan_product"], 1.0)
        write_off_probability *= STATE_STRESS_MULTIPLIER.get(customer["state"], 1.0)
        write_off_probability = max(0.001, min(write_off_probability, 0.24))
        has_matured = months_elapsed >= tenure_months
        default_flag = 0
        write_off_flag = 0
        closure_date = None
        if months_elapsed <= 1:
            loan_status = "Active"
            days_past_due = 0
            current_outstanding = estimate_remaining_balance(
                principal_amount,
                interest_rate,
                tenure_months,
                months_paid_estimate,
            )
        else:
            became_default = np.random.random() < default_probability
            if became_default:
                default_flag = 1
                days_past_due = random.randint(90, 220)
                became_write_off = np.random.random() < write_off_probability
                if became_write_off:
                    write_off_flag = 1
                    loan_status = "Written Off"
                    days_past_due = random.randint(150, 360)
                    remaining_balance = estimate_remaining_balance(
                        principal_amount,
                        interest_rate,
                        tenure_months,
                        max(0, months_paid_estimate - random.randint(2, 6)),
                    )
                    current_outstanding = round(float(remaining_balance * np.random.uniform(0.65, 1.05)), 2)
                    closure_date = None
                else:
                    loan_status = "Defaulted"
                    remaining_balance = estimate_remaining_balance(
                        principal_amount,
                        interest_rate,
                        tenure_months,
                        max(0, months_paid_estimate - random.randint(1, 4)),
                    )
                    current_outstanding = round(float(remaining_balance * np.random.uniform(0.75, 1.15)), 2)
                    closure_date = None
            elif has_matured:
                early_or_normal_close_probability = 0.92
                if np.random.random() < early_or_normal_close_probability:
                    loan_status = "Closed"
                    current_outstanding = 0.0
                    days_past_due = 0
                    closure_lag_days = random.randint(0, 21)
                    maturity_date = disbursement_date + pd.DateOffset(months=tenure_months)
                    closure_date = (maturity_date + timedelta(days=closure_lag_days)).date()
                    if pd.to_datetime(closure_date) > portfolio_end_date:
                        closure_date = portfolio_end_date.date()
                else:
                    loan_status = "Active"
                    days_past_due = assign_dpd_for_active_loan(application["risk_band"], default_probability)
                    current_outstanding = round(float(emi_amount * random.uniform(0.4, 2.2)), 2)
                    closure_date = None
            else:
                loan_status = "Active"
                days_past_due = assign_dpd_for_active_loan(application["risk_band"], default_probability)
                base_outstanding = estimate_remaining_balance(
                    principal_amount,
                    interest_rate,
                    tenure_months,
                    months_paid_estimate,
                )
                if days_past_due == 0:
                    current_outstanding = base_outstanding
                elif days_past_due <= 30:
                    current_outstanding = base_outstanding + emi_amount * np.random.uniform(0.3, 1.2)
                elif days_past_due <= 60:
                    current_outstanding = base_outstanding + emi_amount * np.random.uniform(1.0, 2.2)
                else:
                    current_outstanding = base_outstanding + emi_amount * np.random.uniform(1.8, 3.5)
                current_outstanding = round(float(max(0, current_outstanding)), 2)
                closure_date = None
        loans.append(
            {
                "loan_id": loan_id,
                "application_id": application["application_id"],
                "customer_id": application["customer_id"],
                "disbursement_date": disbursement_date.date(),
                "principal_amount": round(principal_amount, 2),
                "interest_rate": interest_rate,
                "tenure_months": tenure_months,
                "emi_amount": emi_amount,
                "loan_status": loan_status,
                "current_outstanding": round(float(current_outstanding), 2),
                "days_past_due": int(days_past_due),
                "default_flag": int(default_flag),
                "write_off_flag": int(write_off_flag),
                "closure_date": closure_date,
            }
        )
    loans_df = pd.DataFrame(loans)
    # Add a few realistic raw-data quality issues without breaking primary keys.
    missing_closure_idx = loans_df[
        loans_df["loan_status"] == "Closed"
    ].sample(frac=0.01, random_state=RANDOM_SEED + 301).index
    loans_df.loc[missing_closure_idx, "closure_date"] = pd.NaT
    outlier_interest_idx = loans_df.sample(frac=0.001, random_state=RANDOM_SEED + 302).index
    loans_df.loc[outlier_interest_idx, "interest_rate"] = (
        loans_df.loc[outlier_interest_idx, "interest_rate"] + np.random.uniform(4, 8)
    ).round(2)
    return loans_df
def main() -> None:
    loans_df = generate_loans()
    LOANS_FILE.parent.mkdir(parents=True, exist_ok=True)
    loans_df.to_csv(LOANS_FILE, index=False)
    print("loans.csv generated successfully")
    print(f"Output file: {LOANS_FILE}")
    print(f"Rows: {len(loans_df):,}")
    print(f"Columns: {loans_df.shape[1]}")
    print("")
    print("Loan status distribution:")
    print(loans_df["loan_status"].value_counts().to_string())
    print("")
    print("Default and write-off counts:")
    print(f"Defaulted loans: {int(loans_df['default_flag'].sum()):,}")
    print(f"Written-off loans: {int(loans_df['write_off_flag'].sum()):,}")
    print("")
    print("Current outstanding summary:")
    print(loans_df["current_outstanding"].describe().round(2).to_string())
    print("")
    print("Sample records:")
    print(loans_df.head(5).to_string(index=False))
if __name__ == "__main__":
    main()
