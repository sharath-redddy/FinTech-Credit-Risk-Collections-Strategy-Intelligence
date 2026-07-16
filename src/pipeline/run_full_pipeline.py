import subprocess
import sys
from datetime import datetime
PIPELINE_STEPS = [
    ("Generate customers", "src.data_generation.generate_customers"),
    ("Generate loan applications", "src.data_generation.generate_loan_applications"),
    ("Generate loans", "src.data_generation.generate_loans"),
    ("Generate repayment transactions", "src.data_generation.generate_repayment_transactions"),
    ("Generate delinquency snapshots", "src.data_generation.generate_delinquency_snapshots"),
    ("Generate collections actions", "src.data_generation.generate_collections_actions"),
    ("Generate credit policy simulations", "src.data_generation.generate_credit_policy_simulations"),
    ("Generate daily portfolio metrics", "src.data_generation.generate_daily_portfolio_metrics"),
    ("Validate raw data", "src.data_validation.validate_raw_data"),
    ("Clean raw data", "src.data_processing.clean_raw_data"),
    ("Create corrected cleaning summary", "src.data_processing.create_corrected_cleaning_summary"),
    ("Create analytics marts", "src.analytics.create_analytics_marts"),
    ("Train default risk model", "src.modeling.train_default_risk_model"),
    ("Create credit risk strategy marts", "src.analytics.create_credit_risk_strategy_marts"),
]
def run_step(step_name: str, module_name: str) -> None:
    print("=" * 90)
    print(f"STARTING: {step_name}")
    print("=" * 90)
    result = subprocess.run(
        [sys.executable, "-m", module_name],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at step: {step_name}")
    print("")
    print(f"COMPLETED: {step_name}")
    print("")
def main() -> None:
    start_time = datetime.now()
    print("")
    print("CrediSphere Finance - Credit Risk Project Pipeline")
    print(f"Pipeline started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    for step_name, module_name in PIPELINE_STEPS:
        run_step(step_name, module_name)
    end_time = datetime.now()
    duration = end_time - start_time
    print("=" * 90)
    print("FULL PROJECT PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 90)
    print(f"Started at:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration:    {duration}")
    print("")
    print("Generated outputs:")
    print("- data/raw")
    print("- data/processed")
    print("- data/marts")
    print("- outputs/reports")
    print("- models")
    print("")
    print("Note: Power BI dashboard is intentionally not included in this pipeline.")
    print("")
if __name__ == "__main__":
    main()
