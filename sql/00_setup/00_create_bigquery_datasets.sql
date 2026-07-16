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
