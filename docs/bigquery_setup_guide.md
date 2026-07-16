# BigQuery Setup Guide
## Purpose
This guide explains how to upload the cleaned CrediSphere Finance datasets into Google BigQuery.
## BigQuery Dataset Structure
The project uses four BigQuery datasets:
| Dataset | Purpose |
|---|---|
| credit_risk_raw | Clean CSV uploads from local processed data |
| credit_risk_staging | Typed staging views |
| credit_risk_clean | Clean analytical warehouse views |
| credit_risk_marts | SQL-based marts for BI analysis |
## Files Uploaded to BigQuery
The upload script loads these local files from data/processed:
- customers_clean.csv
- loan_applications_clean.csv
- loans_clean.csv
- repayment_transactions_clean.csv
- delinquency_snapshots_clean.csv
- collections_actions_clean.csv
- credit_policy_simulations_clean.csv
- daily_portfolio_metrics_clean.csv
## Authentication Requirement
Before running the upload script, Google Cloud authentication must be configured on the laptop.
Recommended command:
    gcloud auth application-default login
## Upload Command Format
Replace YOUR_GCP_PROJECT_ID with the actual Google Cloud project ID.
    python -m src.warehouse.load_processed_data_to_bigquery --project-id YOUR_GCP_PROJECT_ID --location US
## After Upload
Run the SQL scripts in this order:
1. sql/00_setup/00_create_bigquery_datasets.sql
2. sql/01_staging/01_create_staging_views.sql
3. sql/02_cleaning/02_create_clean_views.sql
4. sql/03_analytics_marts/03_create_bigquery_analytics_marts.sql
5. sql/04_validation/04_bigquery_validation_checks.sql
Before running SQL scripts, replace:
    YOUR_GCP_PROJECT_ID
with your real Google Cloud project ID.
## Important Notes
- Generated CSV files are not stored in GitHub because they are excluded by .gitignore.
- The uploaded data is synthetic and created only for portfolio and learning purposes.
- BigQuery upload is optional for local development, but useful for demonstrating warehouse skills.
- Use Power BI later from either BigQuery or local CSV marts, depending on your setup.
