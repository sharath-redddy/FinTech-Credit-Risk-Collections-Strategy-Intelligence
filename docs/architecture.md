# Project Architecture
## Project
FinTech Credit Risk & Collections Strategy Intelligence
## Company
CrediSphere Finance
## Architecture Summary
This project follows a realistic analytics workflow:
1. Synthetic lending data generation
2. Raw data validation
3. Data cleaning and processing
4. Analytics mart creation
5. Default-risk modeling
6. Expected credit loss calculation
7. Collections prioritization
8. Credit policy simulation
9. BigQuery warehouse scripts
10. Streamlit strategy assistant
11. Power BI dashboard, to be completed separately
## Local Folder Flow
data/raw
Stores synthetic raw CSV datasets.
data/processed
Stores cleaned datasets after validation and cleaning.
data/marts
Stores analytics-ready tables for Power BI, Streamlit, and business analysis.
outputs/reports
Stores validation reports, model metrics, feature importance, and mart summaries.
models
Stores the trained default-risk model.
sql
Stores BigQuery setup, staging, cleaning, analytics mart, and validation SQL scripts.
src
Stores all Python source code.
streamlit_app
Stores the Credit Risk Strategy Assistant app.
## Main Pipeline
The full local project pipeline is:
python -m src.pipeline.run_full_pipeline
This regenerates:
- Raw datasets
- Validation reports
- Processed datasets
- Analytics marts
- Default-risk model
- Strategy marts
## BigQuery Layer
The BigQuery warehouse uses four datasets:
- credit_risk_raw
- credit_risk_staging
- credit_risk_clean
- credit_risk_marts
SQL scripts are stored in the sql folder and should be run in sequence.
## Final Analytics Outputs
Key final marts:
- mart_credit_risk_strategy.csv
- mart_executive_kpis.csv
- mart_risk_alerts.csv
- mart_collections_work_queue.csv
- mart_roll_rate_monthly.csv
- mart_vintage_analysis.csv
- mart_segment_performance.csv
- mart_default_risk_predictions.csv
