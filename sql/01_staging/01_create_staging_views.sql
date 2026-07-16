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
