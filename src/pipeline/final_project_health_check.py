from pathlib import Path
import py_compile
import sys
import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "docs/architecture.md",
    "docs/bigquery_setup_guide.md",
    "docs/business_assumptions.md",
    "docs/business_recommendations.md",
    "docs/career_materials.md",
    "docs/data_dictionary.md",
    "docs/model_documentation.md",
    "docs/project_design_direction.md",
    "docs/responsible_lending_notes.md",
    "docs/run_guide.md",
    "src/config.py",
    "src/pipeline/run_full_pipeline.py",
    "src/warehouse/load_processed_data_to_bigquery.py",
    "streamlit_app/app.py",
    "sql/00_setup/00_create_bigquery_datasets.sql",
    "sql/01_staging/01_create_staging_views.sql",
    "sql/02_cleaning/02_create_clean_views.sql",
    "sql/03_analytics_marts/03_create_bigquery_analytics_marts.sql",
    "sql/04_validation/04_bigquery_validation_checks.sql",
]
RAW_FILES = {
    "data/raw/customers.csv": 25000,
    "data/raw/loan_applications.csv": 35000,
    "data/raw/loans.csv": 20000,
    "data/raw/repayment_transactions.csv": 100000,
    "data/raw/delinquency_snapshots.csv": 100000,
    "data/raw/collections_actions.csv": 70000,
    "data/raw/credit_policy_simulations.csv": 8,
    "data/raw/daily_portfolio_metrics.csv": 900,
}
PROCESSED_FILES = {
    "data/processed/customers_clean.csv": 25000,
    "data/processed/loan_applications_clean.csv": 35000,
    "data/processed/loans_clean.csv": 20000,
    "data/processed/repayment_transactions_clean.csv": 100000,
    "data/processed/delinquency_snapshots_clean.csv": 100000,
    "data/processed/collections_actions_clean.csv": 70000,
    "data/processed/credit_policy_simulations_clean.csv": 8,
    "data/processed/daily_portfolio_metrics_clean.csv": 900,
}
MART_FILES = {
    "data/marts/mart_loan_risk_base.csv": 20000,
    "data/marts/mart_collections_work_queue.csv": 5000,
    "data/marts/mart_roll_rate_monthly.csv": 300,
    "data/marts/mart_vintage_analysis.csv": 300,
    "data/marts/mart_segment_performance.csv": 20,
    "data/marts/mart_default_risk_predictions.csv": 20000,
    "data/marts/mart_credit_risk_strategy.csv": 20000,
    "data/marts/mart_executive_kpis.csv": 1,
    "data/marts/mart_risk_alerts.csv": 4,
}
REPORT_FILES = [
    "outputs/reports/raw_data_quality_summary.csv",
    "outputs/reports/raw_data_validation_report.md",
    "outputs/reports/cleaning_summary.csv",
    "outputs/reports/corrected_cleaning_summary.csv",
    "outputs/reports/default_risk_model_metrics.csv",
    "outputs/reports/default_risk_feature_importance.csv",
    "outputs/reports/credit_risk_strategy_mart_summary.csv",
]
MODEL_FILES = [
    "models/default_risk_model.pkl",
]
PYTHON_FILES_TO_COMPILE = [
    "src/config.py",
    "src/pipeline/run_full_pipeline.py",
    "src/warehouse/load_processed_data_to_bigquery.py",
    "streamlit_app/app.py",
]
def pass_check(message: str) -> None:
    print(f"PASS: {message}")
def fail_check(message: str, failures: list[str]) -> None:
    print(f"FAIL: {message}")
    failures.append(message)
def check_required_files(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING REQUIRED PROJECT FILES")
    print("=" * 90)
    for relative_path in REQUIRED_FILES:
        file_path = PROJECT_ROOT / relative_path
        if file_path.exists():
            pass_check(relative_path)
        else:
            fail_check(f"Missing file: {relative_path}", failures)
def check_readme(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING README")
    print("=" * 90)
    readme_path = PROJECT_ROOT / "README.md"
    if not readme_path.exists():
        fail_check("README.md missing", failures)
        return
    text = readme_path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    fence_count = text.count("```")
    if line_count >= 120:
        pass_check(f"README length looks strong: {line_count} lines")
    else:
        fail_check(f"README too short: {line_count} lines", failures)
    if fence_count == 0:
        pass_check("README has no risky broken markdown code fences")
    else:
        fail_check(f"README contains markdown code fences: {fence_count}", failures)
    required_phrases = [
        "Project Overview",
        "Business Problem",
        "Expected Credit Loss",
        "Collections Strategy",
        "Credit Policy Simulator",
        "How to Run the Project",
        "Pending:",
        "Power BI executive dashboard",
    ]
    for phrase in required_phrases:
        if phrase in text:
            pass_check(f"README contains section or phrase: {phrase}")
        else:
            fail_check(f"README missing section or phrase: {phrase}", failures)
def check_csv_group(group_name: str, file_map: dict[str, int], failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print(f"CHECKING {group_name.upper()}")
    print("=" * 90)
    for relative_path, minimum_rows in file_map.items():
        file_path = PROJECT_ROOT / relative_path
        if not file_path.exists():
            fail_check(f"Missing CSV: {relative_path}", failures)
            continue
        try:
            df = pd.read_csv(file_path)
            rows = len(df)
            cols = len(df.columns)
            missing = int(df.isna().sum().sum())
            if rows >= minimum_rows:
                pass_check(f"{relative_path}: {rows:,} rows, {cols} columns")
            else:
                fail_check(
                    f"{relative_path}: only {rows:,} rows, expected at least {minimum_rows:,}",
                    failures,
                )
            if "data/marts" in relative_path and missing == 0:
                pass_check(f"{relative_path}: no missing values")
            elif "data/marts" in relative_path and missing > 0:
                fail_check(f"{relative_path}: {missing:,} missing values", failures)
        except Exception as exc:
            fail_check(f"Could not read {relative_path}: {exc}", failures)
def check_reports_and_model(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING REPORTS AND MODEL")
    print("=" * 90)
    for relative_path in REPORT_FILES:
        file_path = PROJECT_ROOT / relative_path
        if file_path.exists():
            pass_check(relative_path)
        else:
            fail_check(f"Missing report: {relative_path}", failures)
    for relative_path in MODEL_FILES:
        file_path = PROJECT_ROOT / relative_path
        if file_path.exists() and file_path.stat().st_size > 0:
            pass_check(f"{relative_path}: model file exists")
        else:
            fail_check(f"Missing or empty model file: {relative_path}", failures)
def check_model_metrics(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING MODEL METRICS")
    print("=" * 90)
    metrics_path = PROJECT_ROOT / "outputs/reports/default_risk_model_metrics.csv"
    if not metrics_path.exists():
        fail_check("Model metrics file missing", failures)
        return
    metrics = pd.read_csv(metrics_path)
    roc_auc = None
    recall = None
    if "roc_auc" in metrics.columns:
        roc_auc = float(metrics.loc[0, "roc_auc"])
    if "recall" in metrics.columns:
        recall = float(metrics.loc[0, "recall"])
    if roc_auc is None and {"metric", "value"}.issubset(metrics.columns):
        metric_lookup = dict(zip(metrics["metric"], metrics["value"]))
        if "roc_auc" in metric_lookup:
            roc_auc = float(metric_lookup["roc_auc"])
        if "recall" in metric_lookup:
            recall = float(metric_lookup["recall"])
    if roc_auc is None and {"Metric", "Value"}.issubset(metrics.columns):
        metric_lookup = dict(zip(metrics["Metric"], metrics["Value"]))
        if "roc_auc" in metric_lookup:
            roc_auc = float(metric_lookup["roc_auc"])
        if "recall" in metric_lookup:
            recall = float(metric_lookup["recall"])
    if roc_auc is None:
        fail_check("Could not read roc_auc from model metrics", failures)
        return
    if recall is None:
        fail_check("Could not read recall from model metrics", failures)
        return
    if roc_auc >= 0.70:
        pass_check(f"ROC-AUC is strong enough for portfolio project: {roc_auc:.4f}")
    else:
        fail_check(f"ROC-AUC too low: {roc_auc:.4f}", failures)
    if recall >= 0.55:
        pass_check(f"Recall is acceptable for default-risk screening: {recall:.4f}")
    else:
        fail_check(f"Recall too low: {recall:.4f}", failures)
def check_strategy_outputs(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING STRATEGY MART OUTPUTS")
    print("=" * 90)
    strategy_path = PROJECT_ROOT / "data/marts/mart_credit_risk_strategy.csv"
    kpi_path = PROJECT_ROOT / "data/marts/mart_executive_kpis.csv"
    alerts_path = PROJECT_ROOT / "data/marts/mart_risk_alerts.csv"
    if not strategy_path.exists() or not kpi_path.exists() or not alerts_path.exists():
        fail_check("One or more strategy mart outputs are missing", failures)
        return
    strategy = pd.read_csv(strategy_path)
    kpis = pd.read_csv(kpi_path)
    alerts = pd.read_csv(alerts_path)
    required_columns = [
        "loan_id",
        "model_risk_band",
        "predicted_default_probability",
        "final_expected_credit_loss",
        "recommended_strategy_action",
        "risk_rank",
    ]
    for column in required_columns:
        if column in strategy.columns:
            pass_check(f"Strategy mart contains column: {column}")
        else:
            fail_check(f"Strategy mart missing column: {column}", failures)
    if len(kpis) == 1:
        pass_check("Executive KPI mart has exactly one summary row")
    else:
        fail_check(f"Executive KPI mart should have 1 row, found {len(kpis)}", failures)
    if len(alerts) >= 4:
        pass_check(f"Risk alerts created: {len(alerts)}")
    else:
        fail_check(f"Too few risk alerts: {len(alerts)}", failures)
    if strategy["model_risk_band"].nunique() == 4:
        pass_check("All four model risk bands are present")
    else:
        fail_check("Not all four model risk bands are present", failures)
def check_python_syntax(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING PYTHON SYNTAX")
    print("=" * 90)
    for relative_path in PYTHON_FILES_TO_COMPILE:
        file_path = PROJECT_ROOT / relative_path
        if not file_path.exists():
            fail_check(f"Missing Python file: {relative_path}", failures)
            continue
        try:
            py_compile.compile(str(file_path), doraise=True)
            pass_check(f"Syntax OK: {relative_path}")
        except Exception as exc:
            fail_check(f"Syntax error in {relative_path}: {exc}", failures)
def main() -> None:
    failures = []
    print("")
    print("CrediSphere Finance - Final Non-Power-BI Project Health Check")
    check_required_files(failures)
    check_readme(failures)
    check_csv_group("raw data", RAW_FILES, failures)
    check_csv_group("processed data", PROCESSED_FILES, failures)
    check_csv_group("analytics marts", MART_FILES, failures)
    check_reports_and_model(failures)
    check_model_metrics(failures)
    check_strategy_outputs(failures)
    check_python_syntax(failures)
    print("")
    print("=" * 90)
    print("FINAL RESULT")
    print("=" * 90)
    if failures:
        print(f"FAILED CHECKS: {len(failures)}")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("ALL NON-POWER-BI PROJECT CHECKS PASSED")
    print("")
    print("Non-Power-BI project work is complete except final GitHub polish.")
    print("Power BI dashboard is intentionally not checked here.")
if __name__ == "__main__":
    main()
