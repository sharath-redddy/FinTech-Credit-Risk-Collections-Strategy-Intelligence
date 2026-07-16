# Business Assumptions
## Project Title
FinTech Credit Risk & Collections Strategy Intelligence
## Company Name
CrediSphere Finance
## Company Description
CrediSphere Finance is a fictional Indian digital lending company that provides short-term and installment personal loans to salaried and self-employed borrowers.
The company offers credit through digital channels and wants to improve loan approval quality, default-risk identification, delinquency monitoring, collections prioritization, portfolio profitability, and responsible lending governance.
## Business Objective
The main objective of this project is to build an end-to-end credit risk and collections analytics platform that helps leadership answer the following questions:
1. Which applicants are most likely to default?
2. Which approved loans are moving toward delinquency?
3. Which customers should collections teams contact first?
4. Which risk segments create the highest expected credit loss?
5. Which loan channels, regions, occupations, and products have the highest risk?
6. What happens if lending approval thresholds become stricter or looser?
7. Can losses be reduced without rejecting too many good borrowers?
8. Are there potential fairness risks in the approval or risk-scoring process?
9. What actions should leadership take to improve portfolio health?
## Lending Products
CrediSphere offers four fictional loan products:
| Loan Product | Description |
|---|---|
| Personal Loan | Medium-ticket unsecured personal loan for general expenses |
| Salary Advance | Short-term loan for salaried customers before payday |
| Consumer Durable Loan | Loan for electronics, appliances, and household purchases |
| Business Micro-loan | Small business loan for self-employed customers and micro-entrepreneurs |
## Geographic Scope
The synthetic portfolio represents customers across selected Indian states and major cities.
The project will include regional differences in:
- Income levels
- Borrowing demand
- Loan product mix
- Delinquency risk
- Collection performance
## Customer Segments
Customers will be generated across realistic employment and occupation categories:
- Salaried
- Self-employed
- Gig worker
- Small business owner
- Contract worker
Occupation categories may include:
- IT and services
- Sales and retail
- Education
- Healthcare
- Manufacturing
- Transport and logistics
- Small business
- Other services
## Data Time Period
The synthetic dataset will cover at least 30 months of activity.
Planned activity window:
- Start date: 2024-01-01
- End date: 2026-06-30
This gives enough history to analyze:
- Loan application trends
- Disbursement trends
- Repayment behavior
- Delinquency movement
- Vintage performance
- Collections recovery
- Policy simulation impact
## Approval Logic Assumptions
Loan approval will be influenced by:
- Credit score
- Monthly income
- Debt-to-income ratio
- Employment type
- Years employed
- Bank account age
- Requested loan amount
- Requested tenure
- Loan-to-income ratio
- Product type
- Underwriting score
Applicants with stronger credit profiles will generally have higher approval probability.
Applicants with very high debt burden, low credit score, unstable employment, or excessive requested loan amount will have higher rejection probability.
## Rejection Reasons
Possible rejection reasons include:
- Low credit score
- High debt-to-income ratio
- Insufficient income
- Unstable employment history
- High requested loan amount
- Thin banking history
- Policy rule decline
## Risk Band Logic
Applications and loans will be grouped into four risk bands:
| Risk Band | Meaning |
|---|---|
| Low | Strong credit profile and low expected default risk |
| Medium | Acceptable profile with moderate risk |
| High | Weak profile requiring monitoring |
| Critical | Very high-risk profile with elevated default probability |
Risk bands will be influenced by underwriting score, credit score, debt-to-income ratio, employment type, income, tenure, and loan product.
## Delinquency Logic
Loan repayment behavior will follow realistic delinquency movement:
Current ? 1-30 DPD ? 31-60 DPD ? 61-90 DPD ? 90+ DPD ? Default / Write-off
DPD means days past due.
Higher-risk borrowers will have higher probability of:
- Late payments
- Partial payments
- Missed payments
- Rolling forward into worse delinquency buckets
- Defaulting
- Being written off
## Default Definition
For this project, a loan is considered defaulted when it reaches severe delinquency or crosses a risk-defined threshold, usually around 90+ days past due.
## Write-off Definition
A loan may be written off when the outstanding balance is considered unlikely to be recovered after prolonged delinquency and failed collection attempts.
## Expected Credit Loss Assumption
Expected Credit Loss will be calculated as:
Expected Credit Loss = Probability of Default × Loss Given Default × Exposure at Default
Where:
- Probability of Default is estimated from the risk model
- Loss Given Default is the estimated percentage of exposure not recovered
- Exposure at Default is the current outstanding loan balance
## Collections Strategy Assumptions
Collections priority will be based on:
- Probability of default
- Outstanding balance
- Days past due
- Delinquency bucket
- Previous payment behavior
- Promise-to-pay history
- Collection contact outcomes
- Expected recoverable value
Collection actions may include:
- SMS reminder
- WhatsApp reminder
- Phone call
- Email notice
- Field follow-up
- Settlement offer
- Legal review
## Seasonality Assumptions
The synthetic data will include realistic seasonal behavior:
- Higher borrowing demand around festival and shopping periods
- Higher consumer durable loans during promotion-heavy months
- Higher repayment stress after major spending periods
- Possible regional delinquency spike during one selected period
## Data Quality Assumptions
The raw data will intentionally include some issues so the project has meaningful cleaning and validation work.
Planned data-quality issues:
- Missing values
- Duplicate records
- Late payments
- Partial payments
- Outlier loan amounts
- Inconsistent repayment behavior
- A small number of delayed transaction records
All issues must remain realistic and should not break the relationships between tables.
## Responsible Lending and Fairness Assumptions
This project uses simulated data only.
Any fairness analysis in this project is for portfolio demonstration and responsible analytics practice. It should not be presented as evidence of real-world bias.
Sensitive attributes should not be used as direct approval rules.
Fairness checks will focus on monitoring differences across available groups and recommending governance practices.
## Important Disclaimer
This is a synthetic analytics project created for portfolio and learning purposes.
It does not represent real customers, real loan decisions, real credit policy, or real-world lending outcomes.
