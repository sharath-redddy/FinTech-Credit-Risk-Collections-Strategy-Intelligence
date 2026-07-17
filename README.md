# FinTech Credit Risk & Collections Strategy Intelligence
## Project Overview
FinTech Credit Risk & Collections Strategy Intelligence is an advanced end-to-end analytics project built for a fictional Indian digital lending company called CrediSphere Finance.
The project analyzes loan applications, approval quality, repayment behavior, delinquency movement, default risk, expected credit loss, collections prioritization, credit policy scenarios, responsible lending monitoring, and executive Power BI reporting.
This project is designed to demonstrate practical skills for Data Analyst, Risk Analyst, Business Analyst, BI Analyst, Analytics Engineer, and Product Analyst roles.
## Business Problem
Digital lenders must grow loan disbursements while controlling credit losses.
CrediSphere Finance wants to answer:
- Which applicants are most likely to default?
- Which approved loans are moving toward delinquency?
- Which borrowers should collections teams contact first?
- Which products, states, channels, and risk bands create the highest loss exposure?
- What happens if approval policy thresholds become stricter or looser?
- Can expected losses be reduced without rejecting too many good borrowers?
- Are there responsible lending risks that need monitoring?
## Project Highlights
- Generated realistic synthetic fintech lending data
- Built raw data validation checks
- Cleaned and standardized all major datasets
- Created analytics marts for credit risk and collections strategy
- Trained a default-risk prediction model
- Calculated expected credit loss
- Built collections priority scoring
- Created credit policy simulation scenarios
- Added BigQuery warehouse SQL scripts
- Built a Streamlit Credit Risk Strategy Assistant
- Built a completed Power BI executive dashboard
- Uploaded generated data, marts, reports, trained model, and PBIX dashboard to GitHub
## Dataset Scale
| Dataset | Approximate Size |
|---|---:|
| Customers | 25,000 |
| Loan Applications | 35,000 |
| Approved Loans | 21,000+ |
| Repayment Transactions | 100,000+ |
| Delinquency Snapshots | 120,000+ |
| Collections Actions | 75,000+ |
| Policy Simulation Scenarios | 8 |
| Daily Portfolio Metrics | 900+ |
## Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- SQL
- Google BigQuery
- Streamlit
- Power BI
- Git and GitHub
## Repository Structure
    FinTech-Credit-Risk-Collections-Strategy-Intelligence/
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── marts/
    ├── docs/
    ├── models/
    ├── outputs/
    │   └── reports/
    ├── powerbi/
    ├── sql/
    ├── src/
    ├── streamlit_app/
    ├── README.md
    ├── requirements.txt
    └── .gitignore
## Main Datasets
| Dataset | Description |
|---|---|
| customers | Customer demographic, employment, income, credit score, and acquisition-channel data |
| loan_applications | Application-level approval, rejection, underwriting, and risk-band data |
| loans | Approved loan portfolio with outstanding balance, DPD, default, and write-off flags |
| repayment_transactions | Installment-level due dates, payments, partial payments, late payments, and missed payments |
| delinquency_snapshots | Monthly delinquency movement and roll-rate tracking |
| collections_actions | Collection attempts, channels, agents, promises to pay, and recovered amounts |
| credit_policy_simulations | Scenario outputs for different credit approval policies |
| daily_portfolio_metrics | Daily executive-level portfolio metrics |
## Final Analytics Marts
| Mart | Purpose |
|---|---|
| mart_loan_risk_base | Base loan-level risk mart |
| mart_default_risk_predictions | Model probability of default and model risk bands |
| mart_credit_risk_strategy | Final strategy-ready risk and expected loss mart |
| mart_executive_kpis | Executive KPI summary |
| mart_risk_alerts | Business-friendly risk alert table |
| mart_collections_work_queue | Ranked collections work queue |
| mart_roll_rate_monthly | Monthly delinquency roll-rate transitions |
| mart_vintage_analysis | Vintage delinquency performance |
| mart_segment_performance | Segment-level portfolio performance |
## Power BI Dashboard
The completed Power BI dashboard is included in this repository.
Power BI file:
    powerbi/CrediSphere_Credit_Risk_Dashboard.pbix
Dashboard pages:
- Executive Credit Risk Command Center
- Delinquency & Roll-Rate Intelligence
- Default Risk & Expected Credit Loss
- Collections Strategy Control Tower
- Credit Policy Simulator & Responsible Lending
## Model Summary
The project trains a Random Forest default-risk model.
Main evaluation metrics:
- ROC-AUC: approximately 0.79
- Recall: approximately 0.66
- F1-score: approximately 0.40
- Default rate: approximately 12%
Accuracy is not treated as the main success metric because default prediction is an imbalanced classification problem.
## Expected Credit Loss Logic
Expected Credit Loss is calculated as:
    Expected Credit Loss = Probability of Default x Loss Given Default x Exposure at Default
This helps prioritize loans and segments based on expected financial exposure, not only default count.
## Collections Strategy
The collections priority score uses:
- Predicted probability of default
- Days past due
- Outstanding balance
- Delinquency bucket
- Promise-to-pay history
- Previous contact attempts
- Expected recoverable value
Recommended collections actions include:
- Digital reminder
- Priority phone call
- Escalated collections follow-up
- Settlement offer
- Legal review
## Credit Policy Simulator
The policy simulator compares lending strategies using:
- Minimum credit score
- Maximum debt-to-income ratio
- Maximum loan-to-income ratio
- Predicted approval rate
- Predicted default rate
- Expected credit loss
- Projected revenue
- Policy recommendation
## BigQuery Usage
The project includes BigQuery SQL scripts for:
- Dataset setup
- Staging views
- Clean warehouse views
- Analytics marts
- Validation checks
BigQuery guide:
    docs/bigquery_setup_guide.md
Upload command format:
    python -m src.warehouse.load_processed_data_to_bigquery --project-id YOUR_GCP_PROJECT_ID --location US
## How to Run the Project
### 1. Create virtual environment
    python -m venv .venv
### 2. Activate virtual environment
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1
### 3. Install requirements
    pip install -r requirements.txt
### 4. Run full local pipeline
    python -m src.pipeline.run_full_pipeline
This regenerates:
- Raw datasets
- Validation reports
- Clean processed datasets
- Analytics marts
- Default-risk model
- Strategy marts
### 5. Run Streamlit app
    streamlit run streamlit_app/app.py
## Final Deliverables Included
This repository includes:
- Source code
- Synthetic raw data
- Cleaned processed data
- Analytics marts
- Validation reports
- Model metrics
- Trained default-risk model
- Streamlit strategy assistant
- BigQuery SQL scripts
- Completed Power BI dashboard file
- Documentation and career materials
## Current Project Status
Completed:
- Project setup
- Data generation
- Data validation
- Data cleaning
- Analytics marts
- Default-risk model
- Expected credit loss logic
- Collections prioritization
- Credit policy simulator
- BigQuery SQL scripts
- BigQuery upload helper
- Streamlit strategy assistant
- Power BI executive dashboard
- Documentation
- GitHub upload
Pending:
- None
## Responsible Lending Note
This project uses synthetic data only.
Fairness checks are included for responsible monitoring practice and should not be presented as evidence of real-world bias.
Sensitive attributes should not be used as direct approval rules.
## Disclaimer
This project uses synthetic data for portfolio and learning purposes.
It does not represent real customers, real loan decisions, real credit policies, or real lending outcomes.
