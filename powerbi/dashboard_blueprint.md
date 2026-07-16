# Power BI Dashboard Blueprint
## Project
FinTech Credit Risk & Collections Strategy Intelligence
## Company
CrediSphere Finance
## Dashboard Style Direction
This dashboard must use a bright, premium fintech risk-intelligence style.
Avoid:
- Dark theme
- Generic student-style visuals
- Crowded pages
- Random colors
- Basic default Power BI layout
Use:
- White or soft-light background
- Blue, teal, emerald, amber, orange, and red risk accents
- Rounded cards
- Strong spacing
- Executive control-tower layout
- Clear business recommendations
- Risk-priority storytelling
## Data Source Options
Recommended for portfolio build:
Option 1:
Use local CSV files from data/marts for Power BI development.
Option 2:
Use BigQuery tables/views after uploading processed files.
For fastest dashboard creation, use local marts first:
- mart_credit_risk_strategy.csv
- mart_executive_kpis.csv
- mart_risk_alerts.csv
- mart_collections_work_queue.csv
- mart_roll_rate_monthly.csv
- mart_vintage_analysis.csv
- mart_segment_performance.csv
- mart_default_risk_predictions.csv
- daily_portfolio_metrics_clean.csv
- credit_policy_simulations_clean.csv
## Required Pages
### Page 1: Executive Credit Risk Command Center
Purpose:
Give leadership a single view of portfolio health, loss exposure, delinquency pressure, and recommended action.
Main visuals:
- KPI cards:
  - Total Portfolio Outstanding
  - Active Loans
  - Default Rate
  - PAR30
  - PAR60
  - PAR90
  - Expected Credit Loss
  - Recovery Rate
- Risk alerts panel
- Portfolio outstanding trend
- Expected credit loss by risk band
- PAR trend
- Executive recommendation card
Decision story:
Where is risk concentrated, how serious is it, and what should leadership do now?
### Page 2: Delinquency & Roll-Rate Intelligence
Purpose:
Explain movement from Current to higher delinquency buckets.
Main visuals:
- Delinquency bucket distribution
- Monthly roll-rate transition matrix
- PAR30 / PAR60 / PAR90 trend
- Vintage analysis by origination month
- Delinquency by product, state, channel, and risk band
Decision story:
Which loans are rolling forward, which cohorts are worsening, and where should monitoring increase?
### Page 3: Default Risk & Expected Loss
Purpose:
Explain model-driven default probability and expected credit loss.
Main visuals:
- Model risk-band distribution
- Expected credit loss by segment
- Top risky loans table
- Predicted default probability distribution
- Feature importance visual
- Default model performance summary
Decision story:
Which loans and segments create the highest future loss exposure?
### Page 4: Collections Strategy Control Tower
Purpose:
Help collections teams prioritize loans and evaluate recovery performance.
Main visuals:
- Collections priority queue
- Recovery by channel
- Recovery by agent
- Contact attempt effectiveness
- Promise-to-pay performance
- Recommended next action by delinquency bucket
Decision story:
Who should collections contact first, using which action, and why?
### Page 5: Credit Policy Simulator & Responsible Lending
Purpose:
Compare lending policies and monitor responsible lending signals.
Main visuals:
- Policy scenario comparison
- Approval rate vs default rate trade-off
- Projected revenue vs expected credit loss
- Recommended policy card
- Approval/default comparison by available groups
- Governance notes
Decision story:
Can CrediSphere reduce losses without rejecting too many good borrowers?
## Bright Theme Color Logic
| Use Case | Color |
|---|---|
| Background | #F8FAFC |
| Card background | #FFFFFF |
| Primary fintech blue | #2563EB |
| Teal accent | #06B6D4 |
| Healthy / Low risk | #10B981 |
| Medium / Watch | #F59E0B |
| High risk | #F97316 |
| Critical risk / Default | #EF4444 |
| Slate text | #334155 |
| Light border | #E2E8F0 |
## Layout Rules
- Use 16:9 canvas.
- Use one clean header per page.
- Keep 5 to 8 major visuals per page.
- Do not overload every page with slicers.
- Use a left or top filter strip.
- Use cards for leadership KPIs.
- Use tables only where action is required.
- Use red only for true risk/default/write-off signals.
- Use amber/orange for warning states.
- Use green only for healthy/low-risk metrics.
## Recommended Slicers
Use consistent slicers across pages:
- Date
- Loan Product
- State
- Risk Band
- Model Risk Band
- Delinquency Bucket
- Employment Type
- Acquisition Channel
## Tooltip Ideas
Add tooltip pages later for:
- Loan-level risk explanation
- Segment expected loss details
- Roll-rate transition explanation
- Collections recommendation logic
## Final Dashboard Standard
The dashboard should look like a real credit-risk command center created for a fintech leadership team, not a beginner portfolio dashboard.
