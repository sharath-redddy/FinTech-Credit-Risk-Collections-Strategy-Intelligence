from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
HEALTH_CHECK_FILE = PROJECT_ROOT / "src" / "pipeline" / "final_project_health_check.py"
old_function = '''def check_model_metrics(failures: list[str]) -> None:
    print("")
    print("=" * 90)
    print("CHECKING MODEL METRICS")
    print("=" * 90)
    metrics_path = PROJECT_ROOT / "outputs/reports/default_risk_model_metrics.csv"
    if not metrics_path.exists():
        fail_check("Model metrics file missing", failures)
        return
    metrics = pd.read_csv(metrics_path)
    if "roc_auc" not in metrics.columns:
        fail_check("roc_auc column missing from model metrics", failures)
        return
    roc_auc = float(metrics.loc[0, "roc_auc"])
    recall = float(metrics.loc[0, "recall"])
    if roc_auc >= 0.70:
        pass_check(f"ROC-AUC is strong enough for portfolio project: {roc_auc:.4f}")
    else:
        fail_check(f"ROC-AUC too low: {roc_auc:.4f}", failures)
    if recall >= 0.55:
        pass_check(f"Recall is acceptable for default-risk screening: {recall:.4f}")
    else:
        fail_check(f"Recall too low: {recall:.4f}", failures)
'''
new_function = '''def check_model_metrics(failures: list[str]) -> None:
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
'''
text = HEALTH_CHECK_FILE.read_text(encoding="utf-8")
if old_function not in text:
    print("Expected old health-check function was not found. No replacement applied.")
else:
    text = text.replace(old_function, new_function)
    HEALTH_CHECK_FILE.write_text(text, encoding="utf-8")
    print("Updated final_project_health_check.py to support both wide and metric/value model metrics formats.")
