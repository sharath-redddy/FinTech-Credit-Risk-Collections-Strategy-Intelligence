import random
from datetime import timedelta
import numpy as np
import pandas as pd
from src.config import (
    LOANS_FILE,
    REPAYMENT_TRANSACTIONS_FILE,
    RANDOM_SEED,
    END_DATE,
)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
PAYMENT_METHODS = [
    "UPI",
    "Auto Debit",
    "Net Banking",
    "Debit Card",
    "Wallet",
    "Cash Collection",
]
PAYMENT_METHOD_WEIGHTS = [0.34, 0.28, 0.14, 0.10, 0.08, 0.06]
def month_difference(start_date: pd.Timestamp, end_date: pd.Timestamp) -> int:
    return max(
        0,
        (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month),
    )
def get_due_date(disbursement_date: pd.Timestamp, installment_number: int) -> pd.Timestamp:
    return disbursement_date + pd.DateOffset(months=installment_number)
def classify_loan_risk_from_status(loan_status: str, days_past_due: int) -> str:
    if loan_status == "Written Off":
        return "Severe"
    if loan_status == "Defaulted":
        return "High"
    if days_past_due >= 61:
        return "High"
    if days_past_due >= 31:
        return "Medium"
    if days_past_due >= 1:
        return "Watch"
    return "Healthy"
def choose_payment_status(loan_status: str, days_past_due: int, installment_number: int, total_installments_due: int) -> str:
    risk_level = classify_loan_risk_from_status(loan_status, days_past_due)
    # Later installments on defaulted loans are more likely to be missed.
    late_stage = installment_number >= max(1, int(total_installments_due * 0.60))
    if loan_status == "Closed":
        return random.choices(
            ["Paid", "Late", "Partial"],
            weights=[0.78, 0.18, 0.04],
            k=1,
        )[0]
    if risk_level == "Healthy":
        return random.choices(
            ["Paid", "Late", "Partial", "Missed"],
            weights=[0.76, 0.17, 0.05, 0.02],
            k=1,
        )[0]
    if risk_level == "Watch":
        return random.choices(
            ["Paid", "Late", "Partial", "Missed"],
            weights=[0.56, 0.28, 0.11, 0.05],
            k=1,
        )[0]
    if risk_level == "Medium":
        return random.choices(
            ["Paid", "Late", "Partial", "Missed"],
            weights=[0.40, 0.30, 0.18, 0.12],
            k=1,
        )[0]
    if risk_level == "High":
        if late_stage:
            return random.choices(
                ["Paid", "Late", "Partial", "Missed"],
                weights=[0.17, 0.25, 0.23, 0.35],
                k=1,
            )[0]
        return random.choices(
            ["Paid", "Late", "Partial", "Missed"],
            weights=[0.34, 0.29, 0.20, 0.17],
            k=1,
        )[0]
    if late_stage:
        return random.choices(
            ["Paid", "Late", "Partial", "Missed"],
            weights=[0.08, 0.16, 0.24, 0.52],
            k=1,
        )[0]
    return random.choices(
        ["Paid", "Late", "Partial", "Missed"],
        weights=[0.24, 0.25, 0.24, 0.27],
        k=1,
    )[0]
def generate_payment_details(
    payment_status: str,
    due_date: pd.Timestamp,
    due_amount: float,
    portfolio_end_date: pd.Timestamp,
) -> tuple[object, float, int, str]:
    payment_method = random.choices(
        PAYMENT_METHODS,
        weights=PAYMENT_METHOD_WEIGHTS,
        k=1,
    )[0]
    if payment_status == "Paid":
        days_late = random.choices(
            [0, 1, 2, 3],
            weights=[0.72, 0.16, 0.08, 0.04],
            k=1,
        )[0]
        payment_date = due_date + timedelta(days=days_late)
        paid_amount = due_amount
    elif payment_status == "Late":
        days_late = random.randint(4, 45)
        payment_date = due_date + timedelta(days=days_late)
        paid_amount = due_amount
    elif payment_status == "Partial":
        days_late = random.randint(0, 60)
        payment_date = due_date + timedelta(days=days_late)
        paid_amount = round(float(due_amount * np.random.uniform(0.20, 0.85)), 2)
    elif payment_status == "Missed":
        days_late = random.randint(31, 120)
        payment_date = None
        paid_amount = 0.0
        payment_method = None
    else:
        days_late = 0
        payment_date = None
        paid_amount = 0.0
        payment_method = None
    if payment_date is not None and payment_date > portfolio_end_date:
        payment_status = "Pending"
        payment_date = None
        paid_amount = 0.0
        days_late = 0
        payment_method = None
    return payment_date, round(float(paid_amount), 2), int(days_late), payment_method
def generate_repayment_transactions() -> pd.DataFrame:
    if not LOANS_FILE.exists():
        raise FileNotFoundError(
            f"Missing loans file: {LOANS_FILE}. Run Step 10 first."
        )
    loans_df = pd.read_csv(LOANS_FILE)
    portfolio_end_date = pd.to_datetime(END_DATE)
    repayments = []
    repayment_counter = 1
    for _, loan in loans_df.iterrows():
        loan_id = loan["loan_id"]
        disbursement_date = pd.to_datetime(loan["disbursement_date"])
        tenure_months = int(loan["tenure_months"])
        emi_amount = float(loan["emi_amount"])
        loan_status = loan["loan_status"]
        days_past_due = int(loan["days_past_due"])
        months_elapsed = month_difference(disbursement_date, portfolio_end_date)
        installments_due = min(tenure_months, max(1, months_elapsed))
        if loan_status == "Closed":
            installments_to_generate = tenure_months
        elif loan_status in ["Defaulted", "Written Off"]:
            installments_to_generate = min(
                tenure_months,
                max(installments_due, int(tenure_months * np.random.uniform(0.55, 0.95))),
            )
        else:
            installments_to_generate = installments_due
        installments_to_generate = max(1, int(installments_to_generate))
        for installment_number in range(1, installments_to_generate + 1):
            due_date = get_due_date(disbursement_date, installment_number)
            if due_date > portfolio_end_date:
                payment_status = "Pending"
                payment_date = None
                paid_amount = 0.0
                days_late = 0
                payment_method = None
            else:
                payment_status = choose_payment_status(
                    loan_status=loan_status,
                    days_past_due=days_past_due,
                    installment_number=installment_number,
                    total_installments_due=installments_to_generate,
                )
                payment_date, paid_amount, days_late, payment_method = generate_payment_details(
                    payment_status=payment_status,
                    due_date=due_date,
                    due_amount=emi_amount,
                    portfolio_end_date=portfolio_end_date,
                )
            repayment_id = f"REPAY{repayment_counter:09d}"
            repayment_counter += 1
            repayments.append(
                {
                    "repayment_id": repayment_id,
                    "loan_id": loan_id,
                    "due_date": due_date.date(),
                    "payment_date": payment_date.date() if payment_date is not None else None,
                    "due_amount": round(float(emi_amount), 2),
                    "paid_amount": round(float(paid_amount), 2),
                    "payment_status": payment_status,
                    "days_late": int(days_late),
                    "payment_method": payment_method,
                }
            )
    repayments_df = pd.DataFrame(repayments)
    # Add small raw-data quality issues for later validation.
    # These duplicates are intentional and will be handled in the cleaning stage.
    duplicate_rows = repayments_df.sample(frac=0.002, random_state=RANDOM_SEED + 401)
    repayments_df = pd.concat([repayments_df, duplicate_rows], ignore_index=True)
    missing_method_idx = repayments_df[
        repayments_df["payment_status"].isin(["Paid", "Late", "Partial"])
    ].sample(frac=0.004, random_state=RANDOM_SEED + 402).index
    repayments_df.loc[missing_method_idx, "payment_method"] = np.nan
    partial_outlier_idx = repayments_df[
        repayments_df["payment_status"] == "Partial"
    ].sample(frac=0.003, random_state=RANDOM_SEED + 403).index
    repayments_df.loc[partial_outlier_idx, "paid_amount"] = (
        repayments_df.loc[partial_outlier_idx, "due_amount"] * np.random.uniform(1.05, 1.30)
    ).round(2)
    return repayments_df
def main() -> None:
    repayments_df = generate_repayment_transactions()
    REPAYMENT_TRANSACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    repayments_df.to_csv(REPAYMENT_TRANSACTIONS_FILE, index=False)
    print("repayment_transactions.csv generated successfully")
    print(f"Output file: {REPAYMENT_TRANSACTIONS_FILE}")
    print(f"Rows: {len(repayments_df):,}")
    print(f"Columns: {repayments_df.shape[1]}")
    print("")
    print("Payment status distribution:")
    print(repayments_df["payment_status"].value_counts().to_string())
    print("")
    print("Payment method distribution:")
    print(repayments_df["payment_method"].value_counts(dropna=False).to_string())
    print("")
    print("Duplicate repayment_id count:")
    print(repayments_df["repayment_id"].duplicated().sum())
    print("")
    print("Sample records:")
    print(repayments_df.head(5).to_string(index=False))
if __name__ == "__main__":
    main()
