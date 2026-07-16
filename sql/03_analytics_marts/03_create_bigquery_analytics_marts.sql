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
