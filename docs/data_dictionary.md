# Data Dictionary
## Project
FinTech Credit Risk & Collections Strategy Intelligence
## Company
CrediSphere Finance
## Purpose
This document defines the synthetic data model used for the credit risk, delinquency, collections, policy simulation, and portfolio intelligence platform.
All data is fictional and created for portfolio and learning purposes.
---
# 1. customers
Customer-level demographic, employment, income, credit, and acquisition information.
| Column | Description |
|---|---|
| customer_id | Unique customer identifier |
| age | Customer age in years |
| gender | Customer gender category used only for cautious fairness monitoring |
| city | Customer city |
| state | Customer state |
| employment_type | Employment type such as salaried, self-employed, gig worker, contract worker, or small business owner |
| occupation_category | Broad occupation group |
| monthly_income | Estimated monthly income in INR |
| credit_score | Simulated bureau-style credit score |
| debt_to_income_ratio | Monthly debt obligation divided by monthly income |
| years_employed | Number of years in current employment or business |
| bank_account_age_months | Age of bank account in months |
| customer_since_date | Date when customer first joined CrediSphere |
| acquisition_channel | Channel through which customer was acquired |
Primary key:
- customer_id
---
# 2. loan_applications
Application-level information for all requested loans, including approvals and rejections.
| Column | Description |
|---|---|
| application_id | Unique loan application identifier |
| customer_id | Customer linked to the application |
| application_date | Date of loan application |
| loan_product | Product requested by customer |
| requested_amount | Requested loan amount in INR |
| requested_tenure_months | Requested loan tenure in months |
| purpose_category | Loan purpose category |
| interest_rate_offered | Offered annual interest rate |
| risk_band | Risk category assigned during underwriting |
| approval_status | Approved or rejected |
| rejection_reason | Reason for rejection if application was rejected |
| approved_amount | Final approved amount if approved |
| approval_date | Date of approval if approved |
| underwriting_score | Internal underwriting score from 0 to 100 |
Primary key:
- application_id
Foreign key:
- customer_id references customers.customer_id
---
# 3. loans
Approved and disbursed loan-level portfolio information.
| Column | Description |
|---|---|
| loan_id | Unique loan identifier |
| application_id | Linked approved application |
| customer_id | Linked customer |
| disbursement_date | Date loan was disbursed |
| principal_amount | Original disbursed principal amount in INR |
| interest_rate | Annual interest rate for the loan |
| tenure_months | Approved loan tenure |
| emi_amount | Scheduled monthly installment amount |
| loan_status | Active, closed, defaulted, or written off |
| current_outstanding | Current outstanding balance |
| days_past_due | Current days past due |
| default_flag | 1 if loan defaulted, otherwise 0 |
| write_off_flag | 1 if loan written off, otherwise 0 |
| closure_date | Loan closure date if closed |
Primary key:
- loan_id
Foreign keys:
- application_id references loan_applications.application_id
- customer_id references customers.customer_id
---
# 4. repayment_transactions
Installment-level repayment schedule and payment behavior.
| Column | Description |
|---|---|
| repayment_id | Unique repayment transaction identifier |
| loan_id | Linked loan |
| due_date | Scheduled installment due date |
| payment_date | Actual payment date |
| due_amount | Scheduled installment amount |
| paid_amount | Actual amount paid |
| payment_status | Paid, late, partial, missed, or pending |
| days_late | Number of days payment was late |
| payment_method | Payment channel used |
Primary key:
- repayment_id
Foreign key:
- loan_id references loans.loan_id
---
# 5. delinquency_snapshots
Periodic loan-level delinquency status snapshots.
| Column | Description |
|---|---|
| snapshot_date | Date of portfolio snapshot |
| loan_id | Linked loan |
| customer_id | Linked customer |
| outstanding_balance | Outstanding balance on snapshot date |
| days_past_due | Days past due on snapshot date |
| delinquency_bucket | Current, 1-30 DPD, 31-60 DPD, 61-90 DPD, 90+ DPD, Default, or Write-off |
| roll_rate_stage | Movement stage used for roll-rate analysis |
| collection_status | Current collection handling status |
| default_flag | 1 if defaulted by snapshot date |
| write_off_flag | 1 if written off by snapshot date |
Composite analytical key:
- snapshot_date
- loan_id
Foreign keys:
- loan_id references loans.loan_id
- customer_id references customers.customer_id
---
# 6. collections_actions
Collections team contact attempts, outcomes, and recovery behavior.
| Column | Description |
|---|---|
| action_id | Unique collection action identifier |
| loan_id | Linked loan |
| customer_id | Linked customer |
| action_date | Date of collection action |
| collection_channel | SMS, WhatsApp, phone call, email, field follow-up, settlement, or legal notice |
| agent_id | Collection agent identifier |
| action_type | Reminder, call, escalation, settlement offer, or legal review |
| promise_to_pay_flag | 1 if borrower promised to pay, otherwise 0 |
| recovered_amount | Amount recovered from the action |
| action_outcome | Contacted, no response, promise to pay, paid, failed, escalated, or settlement accepted |
| contact_attempt_number | Attempt number for that loan |
Primary key:
- action_id
Foreign keys:
- loan_id references loans.loan_id
- customer_id references customers.customer_id
---
# 7. credit_policy_simulations
Scenario-level outputs for credit policy threshold changes.
| Column | Description |
|---|---|
| simulation_id | Unique policy simulation identifier |
| policy_name | Name of simulated policy |
| minimum_credit_score | Minimum credit score threshold |
| maximum_debt_to_income_ratio | Maximum allowed debt-to-income ratio |
| maximum_loan_to_income_ratio | Maximum allowed requested loan amount divided by monthly income |
| predicted_approval_rate | Expected approval rate under policy |
| predicted_default_rate | Expected default rate under policy |
| expected_credit_loss | Estimated expected credit loss under policy |
| projected_revenue | Estimated projected revenue under policy |
| policy_recommendation | Recommendation based on risk-return trade-off |
Primary key:
- simulation_id
---
# 8. daily_portfolio_metrics
Daily aggregated portfolio health and risk metrics.
| Column | Description |
|---|---|
| metric_date | Date of portfolio metric |
| active_loans | Number of active loans |
| new_disbursements | Total value of new disbursements |
| collection_amount | Total collection amount received |
| overdue_balance | Total overdue outstanding balance |
| loans_30_dpd | Number of loans in 30+ DPD |
| loans_60_dpd | Number of loans in 60+ DPD |
| loans_90_dpd | Number of loans in 90+ DPD |
| defaults | Number of defaulted loans |
| write_offs | Number of written-off loans |
| recovery_rate | Collection recovered amount divided by overdue balance |
| expected_credit_loss | Estimated expected credit loss |
| portfolio_revenue | Estimated interest and fee revenue |
Primary key:
- metric_date
---
# Important Notes
- All tables are synthetic.
- Primary and foreign keys must remain internally consistent.
- Sensitive fields must not be used as direct approval rules.
- Gender is included only for cautious simulated fairness monitoring.
- The project must clearly state that fairness results are based on simulated data only.
- Data-quality issues will be intentionally added in raw data but must be tracked and cleaned in later stages.
