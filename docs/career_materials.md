# Career Materials
## Resume-Ready Project Description
Built an end-to-end FinTech Credit Risk & Collections Strategy Intelligence platform for a fictional Indian digital lender, CrediSphere Finance, using Python, SQL, BigQuery, scikit-learn, Streamlit, and Power BI-ready analytics marts.
The project analyzes loan approvals, repayment behavior, delinquency movement, default risk, expected credit loss, collections prioritization, credit policy scenarios, and responsible lending monitoring.
## Resume Bullets
- Developed a synthetic credit-risk analytics platform with 25,000 customers, 35,000 loan applications, 21,000+ approved loans, 100,000+ repayment records, delinquency snapshots, collections actions, and daily portfolio metrics.
- Built a default-risk prediction pipeline using scikit-learn, achieving approximately 0.79 ROC-AUC and approximately 0.66 recall, then converted model probabilities into calibrated Low, Medium, High, and Critical risk bands for portfolio monitoring.
- Created strategy-ready marts for expected credit loss, PAR30/PAR60/PAR90, delinquency roll rates, collections priority scoring, credit policy simulation, risk alerts, and executive reporting.
## GitHub Repository Description
Advanced end-to-end fintech credit risk and collections analytics project using Python, SQL, BigQuery, scikit-learn, Streamlit, and Power BI-ready marts. Includes synthetic lending data generation, risk modeling, expected credit loss, delinquency roll rates, collections prioritization, policy simulation, and responsible lending documentation.
## LinkedIn Portfolio Description
I built an advanced FinTech Credit Risk & Collections Strategy Intelligence project for a fictional Indian digital lender, CrediSphere Finance.
The project simulates a real lending-risk analytics workflow: customer and loan application generation, approval logic, repayment behavior, delinquency movement, default prediction, expected credit loss, collections prioritization, credit policy simulation, BigQuery warehouse scripts, and a Streamlit strategy assistant.
Key highlights:
- 25,000 synthetic customers
- 35,000 loan applications
- 21,000+ approved loans
- 100,000+ repayment records
- Default-risk model with ROC-AUC around 0.79
- Expected credit loss and collections priority scoring
- Policy simulator for approval strategy
- Responsible lending monitoring notes
- Power BI-ready analytics marts
## 60-Second Interview Explanation
This project is an end-to-end credit risk and collections analytics platform for a fictional Indian digital lender called CrediSphere Finance.
I generated realistic synthetic lending data covering customers, loan applications, approved loans, repayments, delinquency snapshots, collections actions, policy simulations, and daily portfolio metrics.
Then I built validation and cleaning pipelines, created analytics marts, trained a default-risk model, calculated expected credit loss, and built collections priority logic.
The project helps answer business questions such as which customers are likely to default, which loans are moving toward delinquency, which accounts collections should prioritize, and how credit policy changes affect approval rate, default rate, revenue, and expected loss.
## 3-Minute Interview Explanation
I built this project to simulate the type of analytics work a credit risk or fintech analytics team would perform at a digital lender.
The fictional company, CrediSphere Finance, offers personal loans, salary advances, consumer durable loans, and business micro-loans. The goal was to improve loan approval quality, default-risk identification, delinquency monitoring, collections prioritization, portfolio profitability, and responsible lending governance.
I started by generating realistic synthetic data with primary and foreign key relationships across customers, loan applications, loans, repayment transactions, delinquency snapshots, collections actions, credit policy simulations, and daily portfolio metrics. The data includes realistic risk drivers such as credit score, debt-to-income ratio, monthly income, employment type, loan amount, tenure, product type, and repayment history.
After data generation, I built validation checks for row counts, nulls, duplicates, primary keys, foreign keys, date ranges, and repayment consistency. I then cleaned the data and created analytics marts for risk analysis, roll-rate movement, vintage performance, segment performance, collections priority, and executive KPIs.
For modeling, I trained a Random Forest default-risk model and evaluated it using ROC-AUC, precision, recall, F1-score, and confusion matrix rather than accuracy alone. I then calibrated the predicted probabilities into Low, Medium, High, and Critical risk bands and calculated expected credit loss using probability of default, loss given default, and exposure at default.
The collections strategy layer ranks loans using risk, outstanding balance, days past due, promise-to-pay history, contact attempts, and expected recoverable value. I also built a policy simulator to compare approval rate, default rate, expected loss, and projected revenue under stricter or looser lending rules.
The project also includes BigQuery warehouse SQL scripts, a Streamlit strategy assistant, responsible lending notes, and professional GitHub documentation. The remaining step is to build the final Power BI executive dashboard using the prepared marts.
## Common Interview Questions and Answers
### Why did you choose this project?
I chose it because credit risk and collections analytics are business-critical areas in fintech. The project is different from basic dashboards because it combines data engineering, risk modeling, expected loss, policy simulation, collections strategy, and executive reporting.
### Why is accuracy not the main metric?
Default prediction is an imbalanced classification problem. A model can achieve high accuracy by mostly predicting non-defaults. Metrics like ROC-AUC, recall, precision, F1-score, and confusion matrix provide a better view of risk-model performance.
### What is Expected Credit Loss?
Expected Credit Loss is calculated as Probability of Default multiplied by Loss Given Default multiplied by Exposure at Default. It estimates the financial loss exposure of a loan or segment.
### How did you prioritize collections?
I created a collections priority score using predicted default risk, days past due, current outstanding balance, promise-to-pay count, previous contact attempts, and expected recoverable value.
### What makes this project realistic?
It includes related lending tables, repayment-level records, delinquency snapshots, roll-rate behavior, default and write-off flags, collection actions, policy scenarios, data-quality issues, validation checks, and business documentation.
### How did you handle responsible lending?
I included fairness-monitoring notes and made it clear that the data is synthetic. Sensitive attributes are not used as direct decision rules. Any group-level differences are treated as monitoring signals, not conclusions.
## Key Business Insights and Recommendations
- Use the Balanced Risk-Return Policy as the preferred approval strategy.
- Prioritize Critical and High model-risk loans for monitoring and collections.
- Track PAR30 as the earliest signal of portfolio stress.
- Use expected credit loss instead of default count alone for risk prioritization.
- Segment collections actions by delinquency bucket.
- Monitor state, product, channel, employment type, and risk-band performance.
- Use responsible lending checks as governance signals, not direct decision rules.
