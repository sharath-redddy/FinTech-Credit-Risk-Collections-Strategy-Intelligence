# Model Documentation
## Model Objective
The default-risk model estimates the probability that an approved loan will default.
## Target Variable
default_flag
- 1 = Loan defaulted
- 0 = Loan did not default
## Model Type
Random Forest Classifier
## Why This Model Was Used
Random Forest was selected because it:
- Handles nonlinear relationships
- Works well with mixed numeric and categorical features
- Provides feature importance
- Is easier to explain than more complex black-box models
- Performs well for synthetic portfolio-risk classification
## Important Features
The model uses:
- Credit score
- Debt-to-income ratio
- Monthly income
- Employment type
- Loan product
- Risk band
- Underwriting score
- Loan amount
- Interest rate
- Tenure
- EMI amount
- Income band
- Acquisition channel
- Purpose category
- State
## Evaluation Metrics
The project reports:
- ROC-AUC
- Precision
- Recall
- F1-score
- Confusion matrix
- Default rate
Accuracy is not used as the main success metric because default prediction is an imbalanced classification problem.
## Risk Bands
Predicted default probabilities are calibrated into percentile-based risk bands:
- Low
- Medium
- High
- Critical
Final distribution:
- Low: approximately 30%
- Medium: approximately 35%
- High: approximately 23%
- Critical: approximately 12%
## Expected Credit Loss
Expected Credit Loss is calculated as:
ECL = Probability of Default × Loss Given Default × Exposure at Default
## Responsible Use
This model is built on synthetic data only.
It should not be used for real lending decisions.
Sensitive attributes should not be used as direct approval rules.
The model is designed for portfolio demonstration, risk analytics learning, and recruiter-facing project presentation.
