from pathlib import Path
# ============================================================
# Project Identity
# ============================================================
PROJECT_NAME = "FinTech Credit Risk & Collections Strategy Intelligence"
COMPANY_NAME = "CrediSphere Finance"
# ============================================================
# Reproducibility
# ============================================================
RANDOM_SEED = 42
# ============================================================
# Synthetic Data Volume Targets
# ============================================================
CUSTOMER_COUNT = 25000
APPLICATION_COUNT = 35000
MIN_APPROVED_LOANS = 20000
# ============================================================
# Activity Window
# ============================================================
START_DATE = "2024-01-01"
END_DATE = "2026-06-30"
# ============================================================
# Project Paths
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"
SQL_DIR = PROJECT_ROOT / "sql"
POWERBI_DIR = PROJECT_ROOT / "powerbi"
STREAMLIT_DIR = PROJECT_ROOT / "streamlit_app"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
# ============================================================
# Raw Dataset Output Files
# ============================================================
CUSTOMERS_FILE = RAW_DATA_DIR / "customers.csv"
LOAN_APPLICATIONS_FILE = RAW_DATA_DIR / "loan_applications.csv"
LOANS_FILE = RAW_DATA_DIR / "loans.csv"
REPAYMENT_TRANSACTIONS_FILE = RAW_DATA_DIR / "repayment_transactions.csv"
DELINQUENCY_SNAPSHOTS_FILE = RAW_DATA_DIR / "delinquency_snapshots.csv"
COLLECTIONS_ACTIONS_FILE = RAW_DATA_DIR / "collections_actions.csv"
CREDIT_POLICY_SIMULATIONS_FILE = RAW_DATA_DIR / "credit_policy_simulations.csv"
DAILY_PORTFOLIO_METRICS_FILE = RAW_DATA_DIR / "daily_portfolio_metrics.csv"
# ============================================================
# Lending Products
# ============================================================
LOAN_PRODUCTS = [
    "Personal Loan",
    "Salary Advance",
    "Consumer Durable Loan",
    "Business Micro-loan",
]
# ============================================================
# Risk Bands
# ============================================================
RISK_BANDS = [
    "Low",
    "Medium",
    "High",
    "Critical",
]
# ============================================================
# Delinquency Buckets
# ============================================================
DELINQUENCY_BUCKETS = [
    "Current",
    "1-30 DPD",
    "31-60 DPD",
    "61-90 DPD",
    "90+ DPD",
    "Default",
    "Write-off",
]
def print_config_summary() -> None:
    """
    Print a short project configuration summary.
    This is used to confirm that the project config is working correctly.
    """
    print("Project configuration loaded successfully")
    print(f"Project: {PROJECT_NAME}")
    print(f"Company: {COMPANY_NAME}")
    print(f"Customers target: {CUSTOMER_COUNT:,}")
    print(f"Applications target: {APPLICATION_COUNT:,}")
    print(f"Minimum approved loans target: {MIN_APPROVED_LOANS:,}")
    print(f"Activity window: {START_DATE} to {END_DATE}")
    print(f"Raw data folder: {RAW_DATA_DIR}")
