# Raw Data Validation Report

## Project
FinTech Credit Risk & Collections Strategy Intelligence

## Validation Summary

- PASS checks: 74
- WARN checks: 6
- FAIL checks: 0

## Raw Dataset Row Counts

| Table | Rows | Columns |
|---|---:|---:|
| customers | 25,000 | 14 |
| loan_applications | 35,000 | 14 |
| loans | 21,693 | 14 |
| repayment_transactions | 114,226 | 9 |
| delinquency_snapshots | 129,726 | 10 |
| collections_actions | 75,578 | 11 |
| credit_policy_simulations | 8 | 10 |
| daily_portfolio_metrics | 912 | 13 |

## Notes

- Repayment transaction duplicates are intentional raw-data quality issues for cleaning practice.
- Missing values in selected non-critical fields are intentional and realistic.
- Foreign keys and critical identifiers should pass validation before moving to BigQuery.

## Failed Checks

No failed checks found.