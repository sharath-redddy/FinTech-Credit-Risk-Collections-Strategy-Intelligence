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
