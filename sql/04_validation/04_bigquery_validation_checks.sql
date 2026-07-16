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
