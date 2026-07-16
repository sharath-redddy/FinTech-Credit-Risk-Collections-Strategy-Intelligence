import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from src.config import (
    CUSTOMER_COUNT,
    CUSTOMERS_FILE,
    RANDOM_SEED,
    START_DATE,
    END_DATE,
)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
STATE_CITY_MAP = {
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"],
    "Telangana": ["Hyderabad", "Warangal", "Karimnagar", "Nizamabad"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur", "Ghaziabad"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Kota"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode", "Thrissur"],
    "Andhra Pradesh": ["Vijayawada", "Visakhapatnam", "Guntur", "Tirupati"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior"],
}
CITY_TIER_MAP = {
    "Bengaluru": "Tier 1",
    "Hyderabad": "Tier 1",
    "Mumbai": "Tier 1",
    "Pune": "Tier 1",
    "Chennai": "Tier 1",
    "New Delhi": "Tier 1",
    "Ahmedabad": "Tier 1",
    "Kolkata": "Tier 1",
    "Noida": "Tier 1",
    "Gurugram": "Tier 1",
}
EMPLOYMENT_TYPES = [
    "Salaried",
    "Self-employed",
    "Gig Worker",
    "Contract Worker",
    "Small Business Owner",
]
OCCUPATION_BY_EMPLOYMENT = {
    "Salaried": [
        "IT and Services",
        "Finance and Accounting",
        "Education",
        "Healthcare",
        "Manufacturing",
        "Sales and Retail",
    ],
    "Self-employed": [
        "Small Business",
        "Professional Services",
        "Sales and Retail",
        "Transport and Logistics",
        "Other Services",
    ],
    "Gig Worker": [
        "Delivery and Mobility",
        "Freelance Services",
        "Transport and Logistics",
        "Other Services",
    ],
    "Contract Worker": [
        "Manufacturing",
        "Construction",
        "Sales and Retail",
        "Operations Support",
        "Other Services",
    ],
    "Small Business Owner": [
        "Small Business",
        "Retail Business",
        "Food and Hospitality",
        "Trading",
        "Services Business",
    ],
}
ACQUISITION_CHANNELS = [
    "Mobile App",
    "Website",
    "Partner Marketplace",
    "DSA Agent",
    "Referral",
    "Paid Search",
    "Social Media",
]
GENDERS = ["Male", "Female", "Other"]
def random_date(start_date: str, end_date: str) -> datetime:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days_between = (end - start).days
    return start + timedelta(days=random.randint(0, days_between))
def choose_state_and_city() -> tuple[str, str]:
    states = list(STATE_CITY_MAP.keys())
    state_weights = [
        0.13,  # Karnataka
        0.12,  # Telangana
        0.14,  # Maharashtra
        0.11,  # Tamil Nadu
        0.08,  # Delhi
        0.08,  # Gujarat
        0.09,  # Uttar Pradesh
        0.06,  # Rajasthan
        0.06,  # West Bengal
        0.05,  # Kerala
        0.05,  # Andhra Pradesh
        0.03,  # Madhya Pradesh
    ]
    state = random.choices(states, weights=state_weights, k=1)[0]
    city = random.choice(STATE_CITY_MAP[state])
    return state, city
def generate_income(employment_type: str, city: str) -> int:
    city_tier = CITY_TIER_MAP.get(city, "Tier 2")
    if employment_type == "Salaried":
        base_income = np.random.normal(62000, 22000)
    elif employment_type == "Self-employed":
        base_income = np.random.normal(58000, 26000)
    elif employment_type == "Small Business Owner":
        base_income = np.random.normal(75000, 38000)
    elif employment_type == "Contract Worker":
        base_income = np.random.normal(39000, 15000)
    else:
        base_income = np.random.normal(34000, 14000)
    if city_tier == "Tier 1":
        base_income *= np.random.uniform(1.10, 1.35)
    else:
        base_income *= np.random.uniform(0.85, 1.05)
    monthly_income = int(max(12000, min(base_income, 350000)))
    return monthly_income
def generate_credit_score(monthly_income: int, employment_type: str, years_employed: float, bank_account_age_months: int) -> int:
    score = 620
    if monthly_income >= 100000:
        score += np.random.normal(55, 25)
    elif monthly_income >= 60000:
        score += np.random.normal(35, 25)
    elif monthly_income >= 35000:
        score += np.random.normal(10, 30)
    else:
        score += np.random.normal(-35, 35)
    if employment_type == "Salaried":
        score += np.random.normal(25, 15)
    elif employment_type == "Small Business Owner":
        score += np.random.normal(5, 20)
    elif employment_type == "Self-employed":
        score += np.random.normal(0, 25)
    elif employment_type == "Contract Worker":
        score += np.random.normal(-25, 25)
    else:
        score += np.random.normal(-35, 30)
    if years_employed >= 5:
        score += 25
    elif years_employed >= 2:
        score += 10
    else:
        score -= 15
    if bank_account_age_months >= 60:
        score += 20
    elif bank_account_age_months < 12:
        score -= 25
    credit_score = int(round(score))
    credit_score = max(300, min(900, credit_score))
    return credit_score
def generate_dti(credit_score: int, employment_type: str) -> float:
    if credit_score >= 760:
        dti = np.random.beta(2.0, 7.0)
    elif credit_score >= 700:
        dti = np.random.beta(2.4, 5.8)
    elif credit_score >= 640:
        dti = np.random.beta(3.0, 4.8)
    else:
        dti = np.random.beta(3.8, 3.5)
    if employment_type in ["Gig Worker", "Contract Worker"]:
        dti += np.random.uniform(0.03, 0.10)
    dti = max(0.02, min(dti, 0.85))
    return round(float(dti), 3)
def generate_customers() -> pd.DataFrame:
    customers = []
    employment_weights = [0.46, 0.20, 0.11, 0.13, 0.10]
    acquisition_weights = [0.34, 0.18, 0.14, 0.12, 0.09, 0.08, 0.05]
    gender_weights = [0.55, 0.43, 0.02]
    for i in range(1, CUSTOMER_COUNT + 1):
        customer_id = f"CUST{i:07d}"
        state, city = choose_state_and_city()
        employment_type = random.choices(EMPLOYMENT_TYPES, weights=employment_weights, k=1)[0]
        occupation_category = random.choice(OCCUPATION_BY_EMPLOYMENT[employment_type])
        age = int(np.random.normal(34, 9))
        age = max(21, min(age, 62))
        years_employed = round(float(np.random.gamma(shape=2.4, scale=2.1)), 1)
        years_employed = max(0.2, min(years_employed, max(0.5, age - 20)))
        bank_account_age_months = int(np.random.gamma(shape=3.0, scale=22))
        bank_account_age_months = max(3, min(bank_account_age_months, 360))
        monthly_income = generate_income(employment_type, city)
        credit_score = generate_credit_score(
            monthly_income=monthly_income,
            employment_type=employment_type,
            years_employed=years_employed,
            bank_account_age_months=bank_account_age_months,
        )
        debt_to_income_ratio = generate_dti(credit_score, employment_type)
        customer_since_date = random_date(START_DATE, END_DATE).date()
        customers.append(
            {
                "customer_id": customer_id,
                "age": age,
                "gender": random.choices(GENDERS, weights=gender_weights, k=1)[0],
                "city": city,
                "state": state,
                "employment_type": employment_type,
                "occupation_category": occupation_category,
                "monthly_income": monthly_income,
                "credit_score": credit_score,
                "debt_to_income_ratio": debt_to_income_ratio,
                "years_employed": years_employed,
                "bank_account_age_months": bank_account_age_months,
                "customer_since_date": customer_since_date,
                "acquisition_channel": random.choices(
                    ACQUISITION_CHANNELS,
                    weights=acquisition_weights,
                    k=1,
                )[0],
            }
        )
    df = pd.DataFrame(customers)
    # Add a few realistic raw-data quality issues.
    # These are intentional and will be handled in later validation and cleaning steps.
    missing_occupation_idx = df.sample(frac=0.006, random_state=RANDOM_SEED).index
    df.loc[missing_occupation_idx, "occupation_category"] = np.nan
    missing_years_idx = df.sample(frac=0.004, random_state=RANDOM_SEED + 1).index
    df.loc[missing_years_idx, "years_employed"] = np.nan
    missing_bank_age_idx = df.sample(frac=0.003, random_state=RANDOM_SEED + 2).index
    df.loc[missing_bank_age_idx, "bank_account_age_months"] = np.nan
    income_outlier_idx = df.sample(frac=0.002, random_state=RANDOM_SEED + 3).index
    df.loc[income_outlier_idx, "monthly_income"] = (
        df.loc[income_outlier_idx, "monthly_income"] * np.random.uniform(2.5, 4.0)
    ).round(0).astype(int)
    return df
def main() -> None:
    customers_df = generate_customers()
    CUSTOMERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    customers_df.to_csv(CUSTOMERS_FILE, index=False)
    print("customers.csv generated successfully")
    print(f"Output file: {CUSTOMERS_FILE}")
    print(f"Rows: {len(customers_df):,}")
    print(f"Columns: {customers_df.shape[1]}")
    print("")
    print("Missing values by column:")
    print(customers_df.isna().sum())
    print("")
    print("Sample records:")
    print(customers_df.head(5).to_string(index=False))
if __name__ == "__main__":
    main()
