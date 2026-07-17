# FinTech Credit Risk & Collections Strategy Intelligence

## Enterprise Credit Risk Analytics | Python, SQL, BigQuery, Machine Learning, Streamlit & Power BI

* * *

## Project Overview

This project is an end-to-end FinTech Credit Risk & Collections Strategy Intelligence platform built for a fictional Indian digital lending company called CrediSphere Finance.

The solution helps credit risk, portfolio, and collections teams evaluate loan approval quality, monitor delinquency movement, estimate default probability, calculate expected credit loss, prioritize collections outreach, compare credit policy scenarios, and communicate portfolio risk through an executive Power BI dashboard.

The project combines synthetic fintech lending data generation, Python validation pipelines, analytics marts, machine learning, expected credit loss logic, collections strategy scoring, BigQuery warehouse scripts, Streamlit, and Power BI into one decision-focused credit risk analytics system.

* * *

## Business Problem

Digital lenders must grow loan disbursements while controlling credit losses, delinquency pressure, and collections cost.

CrediSphere Finance needs to answer:

- Which applicants and approved loans are most likely to default?
- Which products, states, channels, and risk bands create the highest expected loss?
- Which borrowers should collections teams contact first?
- How are loans moving between delinquency buckets over time?
- Which lending policy gives the best balance between approval growth and credit risk?
- How much portfolio exposure is concentrated in Critical and High model-risk loans?
- How can leadership monitor credit risk without relying only on static default counts?

This project solves those questions through a complete analytics and business intelligence workflow.

* * *

## Business Decision

### Question

How should CrediSphere Finance manage loan growth, default risk, expected loss, and collections prioritization across its digital lending portfolio?

### Recommendation

## Balanced Growth With Risk-Weighted Collections

The recommended strategy is to use a Balanced Risk-Return credit policy while prioritizing Critical and High model-risk loans for monitoring and collections.

Key decision logic:

- Use expected credit loss instead of default count alone for risk prioritization.
- Prioritize Critical and High model-risk loans in collections workflows.
- Track PAR30 as the earliest signal of portfolio stress.
- Review product and state-level expected loss concentration.
- Use policy simulation results to avoid overly aggressive growth.
- Keep responsible lending checks as governance monitoring signals.

### Recommended operating strategy

1. Use the Balanced Risk-Return Policy for new originations.
2. Monitor PAR30, PAR60, PAR90, default rate, and expected credit loss at portfolio and segment level.
3. Prioritize collections outreach using risk score, delinquency bucket, outstanding balance, promise-to-pay history, and expected recoverable value.
4. Review Critical and High risk loans weekly.
5. Use state, product, and acquisition channel segmentation to detect concentrated portfolio risk.
6. Treat fairness and responsible lending signals as monitoring indicators, not direct decision rules.

* * *

## Power BI Dashboard

The completed Power BI dashboard is included in the repository.

Open the dashboard here:

    powerbi/CrediSphere_Credit_Risk_Dashboard.pbix

### Dashboard Pages

1. Executive Credit Risk Command Center
2. Delinquency & Roll-Rate Intelligence
3. Default Risk & Expected Credit Loss
4. Collections Strategy Control Tower
5. Credit Policy Simulator & Responsible Lending

### Dashboard Capabilities

The Power BI dashboard includes:

- Executive KPI cards for total loans, active loans, portfolio outstanding, default rate, PAR, and ECL
- Model risk-band distribution and expected credit loss by risk band
- State-level risk concentration
- Delinquency bucket movement and PAR trends
- Monthly roll-rate transition matrix
- Top 25 highest expected-loss loans
- Model-driver table using feature importance
- Collections priority work queue
- Recommended collections action analysis
- Credit policy scenario comparison
- Approval rate versus default rate trade-off visual
- Projected revenue versus expected credit loss comparison
- Responsible lending note for governance context

* * *

## Key Risk Results

| Metric | Result |
|---|---:|
| Total Customers | 25,000 |
| Loan Applications | 35,000 |
| Approved Loans | 21,693 |
| Repayment Transactions | 114,226 raw / 113,998 clean |
| Delinquency Snapshots | 129,726 |
| Collections Actions | 75,578 |
| Daily Portfolio Metrics | 912 |
| Default Rate | Approximately 12% |
| Model ROC-AUC | 0.7885 |
| Model Recall | 0.6610 |
| Final Strategy Mart | 21,693 rows / 56 columns |
| Risk Alerts | 4 |
| Power BI Pages | 5 |

* * *

## Project Scale

| Area | Volume |
|---|---:|
| Customers | 25,000 |
| Loan Applications | 35,000 |
| Approved Loans | 21,693 |
| Raw Repayment Transactions | 114,226 |
| Clean Repayment Transactions | 113,998 |
| Delinquency Snapshots | 129,726 |
| Collections Actions | 75,578 |
| Policy Simulation Scenarios | 8 |
| Daily Portfolio Records | 912 |
| Analytics Marts | 9 |
| Final Dashboard Pages | 5 |

* * *

## What This Project Demonstrates

- Credit risk analytics
- Digital lending portfolio analysis
- Default-risk prediction
- Expected credit loss calculation
- Delinquency bucket analysis
- Roll-rate analytics
- Vintage analysis
- Collections prioritization
- Credit policy simulation
- Responsible lending monitoring
- Python data generation and validation
- SQL and BigQuery warehouse modeling
- Machine learning with scikit-learn
- Executive Power BI dashboard design
- Streamlit decision-assistant development
- Git and GitHub project documentation

* * *

## Architecture

    Synthetic FinTech Lending Data Generation
            |
            v
    Raw CSV Data + Python Validation
            |
            v
    Cleaned Processed Data
            |
            v
    Risk, Delinquency, Collections, and Policy Analytics Marts
            |
            v
    Default-Risk Machine Learning Model
            |
            v
    Expected Credit Loss + Risk Band Calibration
            |
            v
    Strategy Marts + Executive KPIs + Risk Alerts
            |
            +------------------------------------------+
            |                                          |
            v                                          v
    Power BI Executive Dashboard        Streamlit Strategy Assistant

* * *

## Data Model

### Raw Data Sources

| Table | Purpose |
|---|---|
| customers | Customer demographic, employment, income, credit score, and acquisition-channel data |
| loan_applications | Application-level approval, rejection, underwriting, product, and requested amount data |
| loans | Approved loan portfolio with principal, interest rate, EMI, DPD, default, and write-off flags |
| repayment_transactions | Installment-level due dates, payment dates, paid amounts, late payments, partial payments, and missed payments |
| delinquency_snapshots | Monthly loan-level delinquency status, bucket movement, and outstanding balance |
| collections_actions | Collection attempts, channels, agents, promise-to-pay flags, outcomes, and recovered amounts |
| credit_policy_simulations | Approval-policy scenario outputs with approval rate, default rate, ECL, and revenue |
| daily_portfolio_metrics | Daily portfolio-level performance, PAR, recovery, revenue, and loss metrics |

### Core Analytical Table

`mart_credit_risk_strategy` contains one analytical row per approved loan and includes:

- Customer and loan segmentation
- Loan product and geography
- Current outstanding balance
- Days past due and delinquency bucket
- Historical default and write-off flags
- Model probability of default
- Model risk band
- Expected credit loss
- Loss severity classification
- Recommended strategy action
- High-value risk flag
- Risk ranking

* * *

## Credit Risk Metric Definitions

| Metric | Definition |
|---|---|
| Default Rate | Percentage of loans with default flag equal to 1 |
| Write-Off Rate | Percentage of loans written off |
| PAR30 | Percentage of active loans 30+ days past due |
| PAR60 | Percentage of active loans 60+ days past due |
| PAR90 | Percentage of active loans 90+ days past due |
| Probability of Default | Model-estimated probability that a loan will default |
| Expected Credit Loss | Probability of Default × Loss Given Default × Exposure at Default |
| Model Risk Band | Calibrated Low, Medium, High, or Critical risk group based on predicted default probability |
| Collections Priority Score | Ranking score combining risk, exposure, delinquency, contact history, and recoverability |
| Expected Recoverable Value | Estimated recoverable value from prioritized collections action |

* * *

## Analytics Marts

The analytics layer produces the following marts:

| Mart | Purpose |
|---|---|
| mart_loan_risk_base | Base loan-level risk and delinquency mart |
| mart_default_risk_predictions | Model probability of default and calibrated risk bands |
| mart_credit_risk_strategy | Final strategy-ready loan risk and expected loss mart |
| mart_executive_kpis | One-row executive KPI summary |
| mart_risk_alerts | Business-friendly risk alerts and recommendations |
| mart_collections_work_queue | Prioritized collections queue with recommended next action |
| mart_roll_rate_monthly | Monthly delinquency transition matrix |
| mart_vintage_analysis | Vintage performance by origination cohort |
| mart_segment_performance | Segment-level portfolio risk and performance summary |

The final marts are saved in:

    data/marts/

* * *

## Machine Learning Model

A Random Forest classifier was trained to predict loan default risk using borrower, application, and loan-level features.

### Model Objective

Predict the probability that an approved loan will default.

### Target Variable

    default_flag

### Model Performance

| Metric | Score |
|---|---:|
| ROC-AUC | 0.7885 |
| Accuracy | 0.7585 |
| Precision | 0.2824 |
| Recall | 0.6610 |
| F1 Score | 0.3958 |
| Default Rate | 0.1196 |

For default-risk use cases, recall and ROC-AUC are more useful than accuracy alone because the business needs to identify risky borrowers before losses occur.

### Risk Band Calibration

Predicted probabilities are calibrated into portfolio risk bands:

| Risk Band | Approximate Share |
|---|---:|
| Low | 30% |
| Medium | 35% |
| High | 23% |
| Critical | 12% |

* * *

## Expected Credit Loss Framework

Expected Credit Loss is calculated as:

    Expected Credit Loss = Probability of Default × Loss Given Default × Exposure at Default

This allows the business to prioritize loans and segments by estimated financial exposure rather than only by borrower count or default count.

The strategy mart uses ECL to support:

- Critical risk monitoring
- Collections prioritization
- Segment-level exposure analysis
- Policy comparison
- Executive reporting

* * *

## Collections Strategy

The project creates a collections priority work queue using:

- Predicted probability of default
- Current outstanding balance
- Days past due
- Delinquency bucket
- Model risk band
- Promise-to-pay history
- Contact attempt history
- Expected recoverable value

### Recommended Actions

The collections strategy generates recommended next actions such as:

- Digital reminder
- Priority phone call
- Escalated collections follow-up
- Settlement offer
- Legal review

This converts the dashboard from passive reporting into operational decision support for collections teams.

* * *

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

### Policy Decision Use Case

The simulator helps answer:

- What happens if underwriting becomes stricter?
- What happens if the lender expands aggressively?
- Which policy offers the best risk-return balance?
- How much revenue is gained or lost under each scenario?
- How much expected loss is created under each scenario?

* * *

## BigQuery Warehouse Design

The project includes SQL scripts for a BigQuery-style warehouse.

### BigQuery Layers

| Layer | Purpose |
|---|---|
| credit_risk_raw | Clean CSV uploads from local processed data |
| credit_risk_staging | Typed staging views |
| credit_risk_clean | Clean analytical warehouse views |
| credit_risk_marts | SQL-based marts for BI analysis |

### SQL Scripts

| Folder | Purpose |
|---|---|
| sql/00_setup | Dataset creation |
| sql/01_staging | Staging views |
| sql/02_cleaning | Clean analytical views |
| sql/03_analytics_marts | Warehouse marts |
| sql/04_validation | Validation checks |

BigQuery setup guide:

    docs/bigquery_setup_guide.md

Upload command format:

    python -m src.warehouse.load_processed_data_to_bigquery --project-id YOUR_GCP_PROJECT_ID --location US

* * *

## Streamlit Strategy Assistant

The Streamlit app provides an interactive credit risk strategy assistant.

Run it with:

    streamlit run streamlit_app/app.py

The app includes:

- Executive KPI summary
- Portfolio filters
- Risk alerts
- Top high-risk loans
- Collections priority queue
- Policy simulator
- Responsible lending note

App file:

    streamlit_app/app.py

* * *

## Tech Stack

| Layer | Tools |
|---|---|
| Data Generation | Python, Pandas, NumPy, Faker |
| Data Validation | Python validation scripts |
| Data Processing | Python, Pandas |
| Analytics Engineering | Python marts, SQL |
| Cloud Warehouse | Google BigQuery SQL scripts |
| Machine Learning | Scikit-learn, Random Forest |
| BI Dashboard | Power BI |
| Interactive App | Streamlit |
| Documentation | Markdown |
| Version Control | Git, GitHub |

* * *

## Repository Structure

    FinTech-Credit-Risk-Collections-Strategy-Intelligence/
    |
    |-- data/
    |   |-- raw/
    |   |-- processed/
    |   |-- marts/
    |
    |-- docs/
    |   |-- architecture.md
    |   |-- bigquery_setup_guide.md
    |   |-- business_assumptions.md
    |   |-- business_recommendations.md
    |   |-- career_materials.md
    |   |-- data_dictionary.md
    |   |-- model_documentation.md
    |   |-- project_design_direction.md
    |   |-- responsible_lending_notes.md
    |   |-- run_guide.md
    |
    |-- models/
    |   |-- default_risk_model.pkl
    |
    |-- outputs/
    |   |-- reports/
    |
    |-- powerbi/
    |   |-- CrediSphere_Credit_Risk_Dashboard.pbix
    |
    |-- sql/
    |   |-- 00_setup/
    |   |-- 01_staging/
    |   |-- 02_cleaning/
    |   |-- 03_analytics_marts/
    |   |-- 04_validation/
    |
    |-- src/
    |   |-- analytics/
    |   |-- data_generation/
    |   |-- data_processing/
    |   |-- data_validation/
    |   |-- modeling/
    |   |-- pipeline/
    |   |-- warehouse/
    |
    |-- streamlit_app/
    |   |-- app.py
    |
    |-- README.md
    |-- requirements.txt
    |-- .gitignore

* * *

## Run Locally

### 1. Create a virtual environment

    python -m venv .venv

### 2. Activate the virtual environment

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Run the full project pipeline

    python -m src.pipeline.run_full_pipeline

This regenerates:

- Raw datasets
- Validation reports
- Clean processed datasets
- Analytics marts
- Default-risk model
- Strategy marts

### 5. Launch the Streamlit app

    streamlit run streamlit_app/app.py

### 6. Open the Power BI dashboard

    powerbi\CrediSphere_Credit_Risk_Dashboard.pbix

* * *

## Data Quality Controls

The project includes Python validation checks for:

- Duplicate records
- Missing values
- Primary key uniqueness
- Foreign key consistency
- Date range validity
- Approved application to loan consistency
- Repayment transaction quality
- Delinquency snapshot coverage
- Collections action integrity
- Analytics mart completeness
- Model metric availability
- Strategy mart completeness

Final health check result:

    ALL NON-POWER-BI PROJECT CHECKS PASSED

* * *

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

* * *

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

* * *

## Responsible Lending Note

This project uses synthetic data only.

Fairness checks are included for responsible monitoring practice and should not be presented as evidence of real-world bias.

Sensitive attributes should not be used as direct approval rules.

Any group-level difference should be treated as a monitoring signal that requires governance review, not as a final conclusion.

* * *

## Important Disclaimer

CrediSphere Finance is a fictional digital lending company.

All data in this repository is synthetically generated for portfolio and learning purposes.

This project does not represent real customers, real credit decisions, real loan policies, real lending outcomes, or real financial advice.
