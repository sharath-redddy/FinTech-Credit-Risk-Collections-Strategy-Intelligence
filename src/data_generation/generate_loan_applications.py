import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from src.config import (
    APPLICATION_COUNT,
    CUSTOMERS_FILE,
    LOAN_APPLICATIONS_FILE,
    RANDOM_SEED,
    START_DATE,
    END_DATE,
)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
LOAN_PRODUCTS = [
    "Personal Loan",
    "Salary Advance",
    "Consumer Durable Loan",
    "Business Micro-loan",
]
PRODUCT_WEIGHTS = {
    "Personal Loan": 0.38,
    "Salary Advance": 0.24,
    "Consumer Durable Loan": 0.22,
    "Business Micro-loan": 0.16,
}
PURPOSE_BY_PRODUCT = {
    "Personal Loan": [
        "Medical Expense",
        "Education",
        "Travel",
        "Home Improvement",
        "Debt Consolidation",
        "Family Event",
        "Emergency Expense",
    ],
    "Salary Advance": [
        "Monthly Cashflow",
        "Emergency Expense",
        "Rent Payment",
        "Utility Bills",
        "Festival Expense",
    ],
    "Consumer Durable Loan": [
        "Mobile Phone",
        "Laptop",
        "Home Appliance",
        "Furniture",
        "Electronics",
    ],
    "Business Micro-loan": [
        "Working Capital",
        "Inventory Purchase",
        "Equipment Purchase",
        "Shop Renovation",
        "Business Expansion",
    ],
}
ACCEPTED_EMPLOYMENT_FOR_BUSINESS = [
    "Self-employed",
    "Small Business Owner",
    "Gig Worker",
]
STATE_RISK_ADJUSTMENT = {
    "Karnataka": -2,
    "Telangana": -1,
    "Maharashtra": -1,
    "Tamil Nadu": -1,
    "Delhi": 0,
    "Gujarat": 0,
    "Kerala": 0,
    "Andhra Pradesh": 1,
    "West Bengal": 2,
    "Rajasthan": 2,
    "Madhya Pradesh": 3,
    "Uttar Pradesh": 4,
}
EMPLOYMENT_SCORE_ADJUSTMENT = {
    "Salaried": 8,
    "Self-employed": 0,
    "Small Business Owner": -1,
    "Contract Worker": -7,
    "Gig Worker": -9,
}
PRODUCT_SCORE_ADJUSTMENT = {
    "Consumer Durable Loan": 5,
    "Salary Advance": 2,
    "Personal Loan": 0,
    "Business Micro-loan": -4,
}
def parse_date(date_value) -> datetime:
    return pd.to_datetime(date_value).to_pydatetime()
def choose_application_date(customer_since_date: str) -> datetime:
    start = max(parse_date(customer_since_date), datetime.strptime(START_DATE, "%Y-%m-%d"))
    end = datetime.strptime(END_DATE, "%Y-%m-%d")
    if start > end:
        start = datetime.strptime(START_DATE, "%Y-%m-%d")
    all_dates = pd.date_range(start=start, end=end, freq="D")
    month_weights = []
    for date in all_dates:
        month = date.month
        # Higher borrowing around festival/shopping months and year-end spending.
        if month in [9, 10, 11]:
            weight = 1.45
        elif month in [12]:
            weight = 1.25
        elif month in [3, 4]:
            weight = 1.15
        elif month in [1, 2]:
            weight = 0.95
        else:
            weight = 1.00
        # Slightly higher demand around salary dates.
        if date.day in [1, 2, 3, 25, 26, 27, 28]:
            weight *= 1.12
        month_weights.append(weight)
    probabilities = np.array(month_weights, dtype=float)
    probabilities = probabilities / probabilities.sum()
    selected_date = np.random.choice(all_dates, p=probabilities)
    return pd.Timestamp(selected_date).to_pydatetime()
def choose_loan_product(employment_type: str) -> str:
    products = LOAN_PRODUCTS.copy()
    weights = [PRODUCT_WEIGHTS[p] for p in products]
    if employment_type == "Salaried":
        weights = [
            PRODUCT_WEIGHTS["Personal Loan"] + 0.06,
            PRODUCT_WEIGHTS["Salary Advance"] + 0.08,
            PRODUCT_WEIGHTS["Consumer Durable Loan"],
            max(PRODUCT_WEIGHTS["Business Micro-loan"] - 0.14, 0.02),
        ]
    elif employment_type in ["Self-employed", "Small Business Owner"]:
        weights = [
            PRODUCT_WEIGHTS["Personal Loan"],
            max(PRODUCT_WEIGHTS["Salary Advance"] - 0.07, 0.04),
            PRODUCT_WEIGHTS["Consumer Durable Loan"],
            PRODUCT_WEIGHTS["Business Micro-loan"] + 0.10,
        ]
    elif employment_type in ["Gig Worker", "Contract Worker"]:
        weights = [
            PRODUCT_WEIGHTS["Personal Loan"],
            PRODUCT_WEIGHTS["Salary Advance"] + 0.05,
            PRODUCT_WEIGHTS["Consumer Durable Loan"],
            max(PRODUCT_WEIGHTS["Business Micro-loan"] - 0.05, 0.03),
        ]
    weights = np.array(weights, dtype=float)
    weights = weights / weights.sum()
    return random.choices(products, weights=weights, k=1)[0]
def generate_requested_amount(loan_product: str, monthly_income: float) -> int:
    if loan_product == "Salary Advance":
        amount = np.random.uniform(0.25, 0.90) * monthly_income
        amount = max(5000, min(amount, 90000))
    elif loan_product == "Consumer Durable Loan":
        amount = np.random.normal(55000, 26000)
        amount = max(8000, min(amount, 220000))
    elif loan_product == "Business Micro-loan":
        amount = np.random.uniform(2.0, 8.0) * monthly_income
        amount = max(40000, min(amount, 600000))
    else:
        amount = np.random.uniform(1.2, 6.0) * monthly_income
        amount = max(25000, min(amount, 500000))
    # Round to nearest 500.
    rounded_amount = int(round(amount / 500) * 500)
    return rounded_amount
def choose_tenure(loan_product: str) -> int:
    if loan_product == "Salary Advance":
        return random.choices([1, 2, 3, 6], weights=[0.35, 0.25, 0.25, 0.15], k=1)[0]
    if loan_product == "Consumer Durable Loan":
        return random.choices([3, 6, 9, 12, 18, 24], weights=[0.08, 0.25, 0.18, 0.28, 0.13, 0.08], k=1)[0]
    if loan_product == "Business Micro-loan":
        return random.choices([6, 9, 12, 18, 24, 36], weights=[0.10, 0.12, 0.28, 0.20, 0.20, 0.10], k=1)[0]
    return random.choices([6, 9, 12, 18, 24, 36], weights=[0.08, 0.10, 0.28, 0.18, 0.22, 0.14], k=1)[0]
def calculate_underwriting_score(row: pd.Series, loan_product: str, requested_amount: int) -> float:
    credit_score = row["credit_score"]
    monthly_income = row["monthly_income"]
    dti = row["debt_to_income_ratio"]
    years_employed = row["years_employed"]
    bank_age = row["bank_account_age_months"]
    employment_type = row["employment_type"]
    state = row["state"]
    loan_to_income_ratio = requested_amount / max(monthly_income, 1)
    score = 50
    score += (credit_score - 650) / 6.5
    score += min(monthly_income / 10000, 12)
    score -= dti * 38
    score -= max(loan_to_income_ratio - 2.0, 0) * 4.8
    if not pd.isna(years_employed):
        if years_employed >= 5:
            score += 7
        elif years_employed >= 2:
            score += 3
        else:
            score -= 5
    else:
        score -= 3
    if not pd.isna(bank_age):
        if bank_age >= 60:
            score += 5
        elif bank_age < 12:
            score -= 6
    else:
        score -= 3
    score += EMPLOYMENT_SCORE_ADJUSTMENT.get(employment_type, 0)
    score += PRODUCT_SCORE_ADJUSTMENT.get(loan_product, 0)
    score -= STATE_RISK_ADJUSTMENT.get(state, 0)
    if loan_product == "Business Micro-loan" and employment_type not in ACCEPTED_EMPLOYMENT_FOR_BUSINESS:
        score -= 16
    # Add realistic underwriting noise.
    score += np.random.normal(0, 6)
    return round(max(0, min(score, 100)), 2)
def assign_risk_band(underwriting_score: float) -> str:
    if underwriting_score >= 76:
        return "Low"
    if underwriting_score >= 61:
        return "Medium"
    if underwriting_score >= 45:
        return "High"
    return "Critical"
def calculate_interest_rate(risk_band: str, loan_product: str) -> float:
    base_rates = {
        "Salary Advance": 18.5,
        "Consumer Durable Loan": 16.5,
        "Personal Loan": 19.5,
        "Business Micro-loan": 22.0,
    }
    risk_add_on = {
        "Low": 0.0,
        "Medium": 2.5,
        "High": 5.5,
        "Critical": 8.5,
    }
    rate = base_rates[loan_product] + risk_add_on[risk_band] + np.random.normal(0, 0.9)
    return round(float(max(11.0, min(rate, 36.0))), 2)
def approve_or_reject(row: pd.Series, loan_product: str, requested_amount: int, requested_tenure: int, underwriting_score: float) -> tuple[str, str | None, float | None, datetime | None]:
    credit_score = row["credit_score"]
    monthly_income = row["monthly_income"]
    dti = row["debt_to_income_ratio"]
    years_employed = row["years_employed"]
    bank_age = row["bank_account_age_months"]
    employment_type = row["employment_type"]
    loan_to_income_ratio = requested_amount / max(monthly_income, 1)
    hard_rejection_reason = None
    if credit_score < 450:
        hard_rejection_reason = "Low credit score"
    elif dti > 0.84:
        hard_rejection_reason = "High debt-to-income ratio"
    elif monthly_income < 12000 and requested_amount > 120000:
        hard_rejection_reason = "Insufficient income"
    elif loan_to_income_ratio > 13.0:
        hard_rejection_reason = "High requested loan amount"
    elif not pd.isna(bank_age) and bank_age < 2:
        hard_rejection_reason = "Thin banking history"
    elif loan_product == "Business Micro-loan" and employment_type not in ACCEPTED_EMPLOYMENT_FOR_BUSINESS:
        hard_rejection_reason = "Product eligibility mismatch"
    if hard_rejection_reason is not None:
        approval_probability = 0.28
    else:
        approval_probability = 1 / (1 + np.exp(-(underwriting_score - 37) / 8))
        if loan_product == "Consumer Durable Loan":
            approval_probability += 0.05
        elif loan_product == "Business Micro-loan":
            approval_probability -= 0.04
        if requested_tenure >= 24 and loan_to_income_ratio > 4:
            approval_probability -= 0.05
        approval_probability = max(0.18, min(approval_probability, 0.98))
    is_approved = np.random.random() < approval_probability
    if is_approved:
        approval_status = "Approved"
        rejection_reason = None
        if underwriting_score >= 76:
            approved_amount = requested_amount * np.random.uniform(0.90, 1.00)
        elif underwriting_score >= 61:
            approved_amount = requested_amount * np.random.uniform(0.75, 0.95)
        elif underwriting_score >= 45:
            approved_amount = requested_amount * np.random.uniform(0.55, 0.82)
        else:
            approved_amount = requested_amount * np.random.uniform(0.35, 0.65)
        approved_amount = int(round(approved_amount / 500) * 500)
        approved_amount = max(3000, approved_amount)
        approval_lag_days = random.choices([0, 1, 2, 3], weights=[0.42, 0.36, 0.17, 0.05], k=1)[0]
        approval_date = None
        return approval_status, rejection_reason, approved_amount, approval_lag_days
    approval_status = "Rejected"
    if hard_rejection_reason:
        rejection_reason = hard_rejection_reason
    elif underwriting_score < 45:
        rejection_reason = random.choice(["Low credit score", "High debt-to-income ratio", "Policy rule decline"])
    elif dti > 0.58:
        rejection_reason = "High debt-to-income ratio"
    elif loan_to_income_ratio > 6:
        rejection_reason = "High requested loan amount"
    elif pd.isna(years_employed) or years_employed < 0.7:
        rejection_reason = "Unstable employment history"
    elif pd.isna(bank_age) or bank_age < 12:
        rejection_reason = "Thin banking history"
    else:
        rejection_reason = random.choice(
            [
                "Policy rule decline",
                "Insufficient income",
                "High requested loan amount",
                "Unstable employment history",
            ]
        )
    return approval_status, rejection_reason, None, None
def generate_loan_applications() -> pd.DataFrame:
    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Missing customers file: {CUSTOMERS_FILE}. Run Step 8 first."
        )
    customers_df = pd.read_csv(CUSTOMERS_FILE)
    applications = []
    # More active customers can apply more than once, so sampling with replacement is realistic.
    selected_customers = customers_df.sample(
        n=APPLICATION_COUNT,
        replace=True,
        random_state=RANDOM_SEED + 100,
    ).reset_index(drop=True)
    for i, (_, customer) in enumerate(selected_customers.iterrows(), start=1):
        application_id = f"APP{i:08d}"
        loan_product = choose_loan_product(customer["employment_type"])
        requested_amount = generate_requested_amount(loan_product, customer["monthly_income"])
        requested_tenure = choose_tenure(loan_product)
        purpose_category = random.choice(PURPOSE_BY_PRODUCT[loan_product])
        application_date = choose_application_date(customer["customer_since_date"])
        underwriting_score = calculate_underwriting_score(
            row=customer,
            loan_product=loan_product,
            requested_amount=requested_amount,
        )
        risk_band = assign_risk_band(underwriting_score)
        interest_rate_offered = calculate_interest_rate(risk_band, loan_product)
        approval_status, rejection_reason, approved_amount, approval_lag_days = approve_or_reject(
            row=customer,
            loan_product=loan_product,
            requested_amount=requested_amount,
            requested_tenure=requested_tenure,
            underwriting_score=underwriting_score,
        )
        if approval_status == "Approved":
            approval_date = (application_date + timedelta(days=approval_lag_days)).date()
        else:
            approval_date = None
        applications.append(
            {
                "application_id": application_id,
                "customer_id": customer["customer_id"],
                "application_date": application_date.date(),
                "loan_product": loan_product,
                "requested_amount": requested_amount,
                "requested_tenure_months": requested_tenure,
                "purpose_category": purpose_category,
                "interest_rate_offered": interest_rate_offered,
                "risk_band": risk_band,
                "approval_status": approval_status,
                "rejection_reason": rejection_reason,
                "approved_amount": approved_amount,
                "approval_date": approval_date,
                "underwriting_score": underwriting_score,
            }
        )
    applications_df = pd.DataFrame(applications)
    # Add small realistic raw-data quality issues without breaking core IDs.
    missing_purpose_idx = applications_df.sample(frac=0.004, random_state=RANDOM_SEED + 201).index
    applications_df.loc[missing_purpose_idx, "purpose_category"] = np.nan
    missing_channel_like_reason_idx = applications_df[
        applications_df["approval_status"] == "Rejected"
    ].sample(frac=0.006, random_state=RANDOM_SEED + 202).index
    applications_df.loc[missing_channel_like_reason_idx, "rejection_reason"] = np.nan
    outlier_amount_idx = applications_df.sample(frac=0.0015, random_state=RANDOM_SEED + 203).index
    applications_df.loc[outlier_amount_idx, "requested_amount"] = (
        applications_df.loc[outlier_amount_idx, "requested_amount"] * np.random.uniform(1.8, 2.6)
    ).round(0).astype(int)
    return applications_df
def main() -> None:
    applications_df = generate_loan_applications()
    LOAN_APPLICATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    applications_df.to_csv(LOAN_APPLICATIONS_FILE, index=False)
    approved_count = int((applications_df["approval_status"] == "Approved").sum())
    rejected_count = int((applications_df["approval_status"] == "Rejected").sum())
    approval_rate = approved_count / len(applications_df)
    print("loan_applications.csv generated successfully")
    print(f"Output file: {LOAN_APPLICATIONS_FILE}")
    print(f"Rows: {len(applications_df):,}")
    print(f"Columns: {applications_df.shape[1]}")
    print(f"Approved applications: {approved_count:,}")
    print(f"Rejected applications: {rejected_count:,}")
    print(f"Approval rate: {approval_rate:.2%}")
    print("")
    print("Risk band distribution:")
    print(applications_df["risk_band"].value_counts().to_string())
    print("")
    print("Approval status distribution:")
    print(applications_df["approval_status"].value_counts().to_string())
    print("")
    print("Missing values by column:")
    print(applications_df.isna().sum())
    print("")
    print("Sample records:")
    print(applications_df.head(5).to_string(index=False))
if __name__ == "__main__":
    main()


