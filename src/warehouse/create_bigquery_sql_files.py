from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "sql"
FILES = {
    "00_setup/00_create_bigquery_datasets.sql": """
-- ============================================================
-- BigQuery Dataset Setup
-- Project: FinTech Credit Risk & Collections Strategy Intelligence
-- Company: CrediSphere Finance
-- Replace YOUR_GCP_PROJECT_ID with your actual Google Cloud project ID.
-- ============================================================
CREATE SCHEMA IF NOT EXISTS `YOUR_GCP_PROJECT_ID.credit_risk_raw`
OPTIONS (
  location = "US",
  description = "Raw uploaded CSV tables for CrediSphere credit risk project"
);
CREATE SCHEMA IF NOT EXISTS `YOUR_GCP_PROJECT_ID.credit_risk_staging`
OPTIONS (
  location = "US",
  description = "Typed staging views for credit risk warehouse"
);
CREATE SCHEMA IF NOT EXISTS `YOUR_GCP_PROJECT_ID.credit_risk_clean`
OPTIONS (
  location = "US",
  description = "Cleaned analytical views for credit risk warehouse"
);
CREATE SCHEMA IF NOT EXISTS `YOUR_GCP_PROJECT_ID.credit_risk_marts`
OPTIONS (
  location = "US",
  description = "Power BI and Streamlit ready credit risk marts"
);
""",
    "01_staging/01_create_staging_views.sql": """
-- ============================================================
-- BigQuery Staging Views
-- Replace YOUR_GCP_PROJECT_ID with your actual Google Cloud project ID.
-- Raw tables should be uploaded into: credit_risk_raw
-- ============================================================
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_customers` AS
SELECT
  CAST(customer_id AS STRING) AS customer_id,
  CAST(age AS INT64) AS age,
  CAST(gender AS STRING) AS gender,
  CAST(city AS STRING) AS city,
  CAST(state AS STRING) AS state,
  CAST(employment_type AS STRING) AS employment_type,
  CAST(occupation_category AS STRING) AS occupation_category,
  CAST(monthly_income AS NUMERIC) AS monthly_income,
  CAST(credit_score AS INT64) AS credit_score,
  CAST(debt_to_income_ratio AS FLOAT64) AS debt_to_income_ratio,
  CAST(years_employed AS FLOAT64) AS years_employed,
  CAST(bank_account_age_months AS INT64) AS bank_account_age_months,
  CAST(customer_since_date AS DATE) AS customer_since_date,
  CAST(acquisition_channel AS STRING) AS acquisition_channel
FROM `YOUR_GCP_PROJECT_ID.credit_risk_raw.customers_clean`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_loan_applications` AS
SELECT
  CAST(application_id AS STRING) AS application_id,
  CAST(customer_id AS STRING) AS customer_id,
  CAST(application_date AS DATE) AS application_date,
  CAST(loan_product AS STRING) AS loan_product,
  CAST(requested_amount AS NUMERIC) AS requested_amount,
  CAST(requested_tenure_months AS INT64) AS requested_tenure_months,
  CAST(purpose_category AS STRING) AS purpose_category,
  CAST(interest_rate_offered AS FLOAT64) AS interest_rate_offered,
  CAST(risk_band AS STRING) AS risk_band,
  CAST(approval_status AS STRING) AS approval_status,
  CAST(rejection_reason AS STRING) AS rejection_reason,
  CAST(approved_amount AS NUMERIC) AS approved_amount,
  CAST(approval_date AS DATE) AS approval_date,
  CAST(underwriting_score AS FLOAT64) AS underwriting_score
FROM `YOUR_GCP_PROJECT_ID.credit_risk_raw.loan_applications_clean`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_loans` AS
SELECT
  CAST(loan_id AS STRING) AS loan_id,
  CAST(application_id AS STRING) AS application_id,
  CAST(customer_id AS STRING) AS customer_id,
  CAST(disbursement_date AS DATE) AS disbursement_date,
  CAST(principal_amount AS NUMERIC) AS principal_amount,
  CAST(interest_rate AS FLOAT64) AS interest_rate,
  CAST(tenure_months AS INT64) AS tenure_months,
  CAST(emi_amount AS NUMERIC) AS emi_amount,
  CAST(loan_status AS STRING) AS loan_status,
  CAST(current_outstanding AS NUMERIC) AS current_outstanding,
  CAST(days_past_due AS INT64) AS days_past_due,
  CAST(default_flag AS INT64) AS default_flag,
  CAST(write_off_flag AS INT64) AS write_off_flag,
  CAST(closure_date AS DATE) AS closure_date
FROM `YOUR_GCP_PROJECT_ID.credit_risk_raw.loans_clean`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_repayment_transactions` AS
SELECT
  CAST(repayment_id AS STRING) AS repayment_id,
  CAST(loan_id AS STRING) AS loan_id,
  CAST(due_date AS DATE) AS due_date,
  CAST(payment_date AS DATE) AS payment_date,
  CAST(due_amount AS NUMERIC) AS due_amount,
  CAST(paid_amount AS NUMERIC) AS paid_amount,
  CAST(payment_status AS STRING) AS payment_status,
  CAST(days_late AS INT64) AS days_late,
  CAST(payment_method AS STRING) AS payment_method
FROM `YOUR_GCP_PROJECT_ID.credit_risk_raw.repayment_transactions_clean`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_delinquency_snapshots` AS
SELECT
  CAST(snapshot_date AS DATE) AS snapshot_date,
  CAST(loan_id AS STRING) AS loan_id,
  CAST(customer_id AS STRING) AS customer_id,
  CAST(outstanding_balance AS NUMERIC) AS outstanding_balance,
  CAST(days_past_due AS INT64) AS days_past_due,
  CAST(delinquency_bucket AS STRING) AS delinquency_bucket,
  CAST(roll_rate_stage AS STRING) AS roll_rate_stage,
  CAST(collection_status AS STRING) AS collection_status,
  CAST(default_flag AS INT64) AS default_flag,
  CAST(write_off_flag AS INT64) AS write_off_flag
FROM `YOUR_GCP_PROJECT_ID.credit_risk_raw.delinquency_snapshots_clean`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_collections_actions` AS
SELECT
  CAST(action_id AS STRING) AS action_id,
  CAST(loan_id AS STRING) AS loan_id,
  CAST(customer_id AS STRING) AS customer_id,
  CAST(action_date AS DATE) AS action_date,
  CAST(collection_channel AS STRING) AS collection_channel,
  CAST(agent_id AS STRING) AS agent_id,
  CAST(action_type AS STRING) AS action_type,
  CAST(promise_to_pay_flag AS INT64) AS promise_to_pay_flag,
  CAST(recovered_amount AS NUMERIC) AS recovered_amount,
  CAST(action_outcome AS STRING) AS action_outcome,
  CAST(contact_attempt_number AS INT64) AS contact_attempt_number
FROM `YOUR_GCP_PROJECT_ID.credit_risk_raw.collections_actions_clean`;
""",
    "02_cleaning/02_create_clean_views.sql": """
-- ============================================================
-- BigQuery Clean Views
-- Replace YOUR_GCP_PROJECT_ID with your actual Google Cloud project ID.
-- ============================================================
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_clean.dim_customers` AS
SELECT
  customer_id,
  age,
  gender,
  city,
  state,
  employment_type,
  occupation_category,
  monthly_income,
  CASE
    WHEN monthly_income < 25000 THEN "Low Income"
    WHEN monthly_income < 50000 THEN "Mass Market"
    WHEN monthly_income < 100000 THEN "Upper Mass"
    WHEN monthly_income < 200000 THEN "Affluent"
    ELSE "High Income"
  END AS income_band,
  credit_score,
  debt_to_income_ratio,
  years_employed,
  bank_account_age_months,
  customer_since_date,
  acquisition_channel
FROM `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_customers`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loan_applications` AS
SELECT
  application_id,
  customer_id,
  application_date,
  FORMAT_DATE("%Y-%m", application_date) AS application_month,
  loan_product,
  requested_amount,
  requested_tenure_months,
  purpose_category,
  interest_rate_offered,
  risk_band,
  approval_status,
  rejection_reason,
  approved_amount,
  approval_date,
  underwriting_score,
  SAFE_DIVIDE(requested_amount, NULLIF(approved_amount, 0)) AS requested_to_approved_ratio
FROM `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_loan_applications`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loans` AS
SELECT
  loan_id,
  application_id,
  customer_id,
  disbursement_date,
  FORMAT_DATE("%Y-%m", disbursement_date) AS origination_month,
  principal_amount,
  interest_rate,
  tenure_months,
  emi_amount,
  loan_status,
  current_outstanding,
  days_past_due,
  CASE
    WHEN write_off_flag = 1 THEN "Write-off"
    WHEN default_flag = 1 THEN "Default"
    WHEN days_past_due >= 90 THEN "90+ DPD"
    WHEN days_past_due >= 60 THEN "61-90 DPD"
    WHEN days_past_due >= 30 THEN "31-60 DPD"
    WHEN days_past_due > 0 THEN "1-30 DPD"
    ELSE "Current"
  END AS current_delinquency_bucket,
  default_flag,
  write_off_flag,
  closure_date
FROM `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_loans`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_repayments` AS
SELECT
  repayment_id,
  loan_id,
  due_date,
  payment_date,
  due_amount,
  paid_amount,
  payment_status,
  days_late,
  payment_method,
  paid_amount - due_amount AS payment_variance
FROM `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_repayment_transactions`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_delinquency_snapshots` AS
SELECT
  snapshot_date,
  FORMAT_DATE("%Y-%m", snapshot_date) AS snapshot_month,
  loan_id,
  customer_id,
  outstanding_balance,
  days_past_due,
  delinquency_bucket,
  roll_rate_stage,
  collection_status,
  default_flag,
  write_off_flag,
  CASE WHEN days_past_due >= 30 THEN 1 ELSE 0 END AS par30_flag,
  CASE WHEN days_past_due >= 60 THEN 1 ELSE 0 END AS par60_flag,
  CASE WHEN days_past_due >= 90 THEN 1 ELSE 0 END AS par90_flag
FROM `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_delinquency_snapshots`;
CREATE OR REPLACE VIEW `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_collections_actions` AS
SELECT
  action_id,
  loan_id,
  customer_id,
  action_date,
  FORMAT_DATE("%Y-%m", action_date) AS action_month,
  collection_channel,
  agent_id,
  action_type,
  promise_to_pay_flag,
  recovered_amount,
  action_outcome,
  contact_attempt_number
FROM `YOUR_GCP_PROJECT_ID.credit_risk_staging.stg_collections_actions`;
""",
    "03_analytics_marts/03_create_bigquery_analytics_marts.sql": """
-- ============================================================
-- BigQuery Analytics Marts
-- Replace YOUR_GCP_PROJECT_ID with your actual Google Cloud project ID.
-- ============================================================
CREATE OR REPLACE TABLE `YOUR_GCP_PROJECT_ID.credit_risk_marts.mart_portfolio_performance_by_segment` AS
SELECT
  "loan_product" AS segment_type,
  loan_product AS segment_value,
  COUNT(DISTINCT loan_id) AS loans,
  SUM(principal_amount) AS total_principal,
  SUM(current_outstanding) AS outstanding_balance,
  AVG(interest_rate) AS avg_interest_rate,
  AVG(default_flag) AS default_rate,
  AVG(write_off_flag) AS write_off_rate,
  AVG(CASE WHEN days_past_due >= 30 THEN 1 ELSE 0 END) AS par30_rate,
  AVG(CASE WHEN days_past_due >= 60 THEN 1 ELSE 0 END) AS par60_rate,
  AVG(CASE WHEN days_past_due >= 90 THEN 1 ELSE 0 END) AS par90_rate
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loans`
GROUP BY loan_product
UNION ALL
SELECT
  "state" AS segment_type,
  c.state AS segment_value,
  COUNT(DISTINCT l.loan_id) AS loans,
  SUM(l.principal_amount) AS total_principal,
  SUM(l.current_outstanding) AS outstanding_balance,
  AVG(l.interest_rate) AS avg_interest_rate,
  AVG(l.default_flag) AS default_rate,
  AVG(l.write_off_flag) AS write_off_rate,
  AVG(CASE WHEN l.days_past_due >= 30 THEN 1 ELSE 0 END) AS par30_rate,
  AVG(CASE WHEN l.days_past_due >= 60 THEN 1 ELSE 0 END) AS par60_rate,
  AVG(CASE WHEN l.days_past_due >= 90 THEN 1 ELSE 0 END) AS par90_rate
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loans` l
LEFT JOIN `YOUR_GCP_PROJECT_ID.credit_risk_clean.dim_customers` c
  ON l.customer_id = c.customer_id
GROUP BY c.state;
CREATE OR REPLACE TABLE `YOUR_GCP_PROJECT_ID.credit_risk_marts.mart_roll_rate_monthly` AS
WITH ordered_snapshots AS (
  SELECT
    loan_id,
    snapshot_date,
    snapshot_month,
    delinquency_bucket,
    outstanding_balance,
    LAG(delinquency_bucket) OVER (
      PARTITION BY loan_id
      ORDER BY snapshot_date
    ) AS previous_bucket
  FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_delinquency_snapshots`
),
transitions AS (
  SELECT
    snapshot_month,
    previous_bucket,
    delinquency_bucket,
    loan_id,
    outstanding_balance
  FROM ordered_snapshots
  WHERE previous_bucket IS NOT NULL
)
SELECT
  snapshot_month,
  previous_bucket,
  delinquency_bucket,
  COUNT(DISTINCT loan_id) AS transition_count,
  SUM(outstanding_balance) AS outstanding_balance,
  SAFE_DIVIDE(
    COUNT(DISTINCT loan_id),
    SUM(COUNT(DISTINCT loan_id)) OVER (
      PARTITION BY snapshot_month, previous_bucket
    )
  ) AS roll_rate
FROM transitions
GROUP BY
  snapshot_month,
  previous_bucket,
  delinquency_bucket;
CREATE OR REPLACE TABLE `YOUR_GCP_PROJECT_ID.credit_risk_marts.mart_collections_performance` AS
SELECT
  collection_channel,
  agent_id,
  COUNT(DISTINCT action_id) AS total_actions,
  COUNT(DISTINCT loan_id) AS loans_contacted,
  SUM(promise_to_pay_flag) AS promise_to_pay_count,
  SUM(recovered_amount) AS total_recovered_amount,
  AVG(recovered_amount) AS avg_recovered_per_action,
  SAFE_DIVIDE(SUM(recovered_amount), COUNT(DISTINCT loan_id)) AS recovered_per_loan
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_collections_actions`
GROUP BY
  collection_channel,
  agent_id;
CREATE OR REPLACE TABLE `YOUR_GCP_PROJECT_ID.credit_risk_marts.mart_application_funnel` AS
SELECT
  application_month,
  loan_product,
  risk_band,
  COUNT(DISTINCT application_id) AS applications,
  COUNTIF(approval_status = "Approved") AS approved_applications,
  COUNTIF(approval_status = "Rejected") AS rejected_applications,
  SAFE_DIVIDE(COUNTIF(approval_status = "Approved"), COUNT(DISTINCT application_id)) AS approval_rate,
  AVG(requested_amount) AS avg_requested_amount,
  AVG(approved_amount) AS avg_approved_amount,
  AVG(underwriting_score) AS avg_underwriting_score
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loan_applications`
GROUP BY
  application_month,
  loan_product,
  risk_band;
""",
    "04_validation/04_bigquery_validation_checks.sql": """
-- ============================================================
-- BigQuery Warehouse Validation Checks
-- Replace YOUR_GCP_PROJECT_ID with your actual Google Cloud project ID.
-- ============================================================
SELECT
  "customers" AS table_name,
  COUNT(*) AS row_count,
  COUNT(DISTINCT customer_id) AS unique_primary_keys
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.dim_customers`
UNION ALL
SELECT
  "loan_applications" AS table_name,
  COUNT(*) AS row_count,
  COUNT(DISTINCT application_id) AS unique_primary_keys
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loan_applications`
UNION ALL
SELECT
  "loans" AS table_name,
  COUNT(*) AS row_count,
  COUNT(DISTINCT loan_id) AS unique_primary_keys
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loans`
UNION ALL
SELECT
  "repayments" AS table_name,
  COUNT(*) AS row_count,
  COUNT(DISTINCT repayment_id) AS unique_primary_keys
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_repayments`
UNION ALL
SELECT
  "collections_actions" AS table_name,
  COUNT(*) AS row_count,
  COUNT(DISTINCT action_id) AS unique_primary_keys
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_collections_actions`;
-- Foreign key checks
SELECT
  "applications_missing_customer" AS check_name,
  COUNT(*) AS issue_count
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loan_applications` a
LEFT JOIN `YOUR_GCP_PROJECT_ID.credit_risk_clean.dim_customers` c
  ON a.customer_id = c.customer_id
WHERE c.customer_id IS NULL
UNION ALL
SELECT
  "loans_missing_application" AS check_name,
  COUNT(*) AS issue_count
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loans` l
LEFT JOIN `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loan_applications` a
  ON l.application_id = a.application_id
WHERE a.application_id IS NULL
UNION ALL
SELECT
  "repayments_missing_loan" AS check_name,
  COUNT(*) AS issue_count
FROM `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_repayments` r
LEFT JOIN `YOUR_GCP_PROJECT_ID.credit_risk_clean.fact_loans` l
  ON r.loan_id = l.loan_id
WHERE l.loan_id IS NULL;
"""
}
def main() -> None:
    for relative_path, content in FILES.items():
        output_path = SQL_DIR / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content.strip() + "\n", encoding="utf-8")
    print("BigQuery SQL files created successfully.")
    for relative_path in FILES:
        print(f"- sql/{relative_path}")
if __name__ == "__main__":
    main()
