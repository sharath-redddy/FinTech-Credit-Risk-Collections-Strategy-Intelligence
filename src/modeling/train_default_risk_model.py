import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from src.config import PROJECT_ROOT
MARTS_DIR = PROJECT_ROOT / "data" / "marts"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
MODELS_DIR = PROJECT_ROOT / "models"
INPUT_FILE = MARTS_DIR / "mart_loan_risk_base.csv"
MODEL_FILE = MODELS_DIR / "default_risk_model.pkl"
METRICS_FILE = REPORTS_DIR / "default_risk_model_metrics.csv"
FEATURE_IMPORTANCE_FILE = REPORTS_DIR / "default_risk_feature_importance.csv"
PREDICTIONS_FILE = MARTS_DIR / "mart_default_risk_predictions.csv"
NUMERIC_FEATURES = [
    "age",
    "monthly_income",
    "credit_score",
    "debt_to_income_ratio",
    "years_employed",
    "bank_account_age_months",
    "underwriting_score",
    "principal_amount",
    "interest_rate",
    "tenure_months",
    "emi_amount",
    "loan_to_income_ratio",
]
CATEGORICAL_FEATURES = [
    "state",
    "employment_type",
    "occupation_category",
    "income_band",
    "acquisition_channel",
    "loan_product",
    "purpose_category",
    "risk_band",
]
def add_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    customers = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "customers_clean.csv")
    customer_features = customers[
        [
            "customer_id",
            "age",
            "years_employed",
            "bank_account_age_months",
        ]
    ].copy()
    df = df.merge(customer_features, on="customer_id", how="left")
    df["loan_to_income_ratio"] = df["principal_amount"] / df["monthly_income"].clip(lower=1)
    return df
def assign_model_risk_band(probability: float) -> str:
    if probability >= 0.55:
        return "Critical"
    if probability >= 0.35:
        return "High"
    if probability >= 0.16:
        return "Medium"
    return "Low"
def train_model() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_FILE}. Run analytics marts step first."
        )
    df = pd.read_csv(INPUT_FILE)
    df = add_customer_features(df)
    target = "default_flag"
    modeling_df = df[
        [
            "loan_id",
            "customer_id",
            target,
            *NUMERIC_FEATURES,
            *CATEGORICAL_FEATURES,
        ]
    ].copy()
    X = modeling_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = modeling_df[target].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    model = RandomForestClassifier(
        n_estimators=350,
        max_depth=12,
        min_samples_leaf=20,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_probability = pipeline.predict_proba(X_test)[:, 1]
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    metrics = pd.DataFrame(
        [
            {"metric": "rows_total", "value": len(df)},
            {"metric": "train_rows", "value": len(X_train)},
            {"metric": "test_rows", "value": len(X_test)},
            {"metric": "default_rate", "value": round(y.mean(), 4)},
            {"metric": "roc_auc", "value": round(roc_auc_score(y_test, y_probability), 4)},
            {"metric": "accuracy", "value": round(accuracy_score(y_test, y_pred), 4)},
            {"metric": "precision", "value": round(precision_score(y_test, y_pred), 4)},
            {"metric": "recall", "value": round(recall_score(y_test, y_pred), 4)},
            {"metric": "f1_score", "value": round(f1_score(y_test, y_pred), 4)},
            {"metric": "true_negative", "value": int(tn)},
            {"metric": "false_positive", "value": int(fp)},
            {"metric": "false_negative", "value": int(fn)},
            {"metric": "true_positive", "value": int(tp)},
        ]
    )
    onehot = pipeline.named_steps["preprocessor"].named_transformers_["cat"].named_steps["onehot"]
    encoded_cat_features = onehot.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    feature_names = NUMERIC_FEATURES + encoded_cat_features
    importances = pipeline.named_steps["model"].feature_importances_
    feature_importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    ).sort_values("importance", ascending=False)
    all_probabilities = pipeline.predict_proba(X)[:, 1]
    predictions = df[
        [
            "loan_id",
            "customer_id",
            "state",
            "employment_type",
            "loan_product",
            "risk_band",
            "principal_amount",
            "current_outstanding",
            "default_flag",
            "write_off_flag",
        ]
    ].copy()
    predictions["predicted_default_probability"] = np.round(all_probabilities, 4)
    predictions["model_risk_band"] = predictions["predicted_default_probability"].apply(assign_model_risk_band)
    predictions["loss_given_default"] = np.where(
        predictions["write_off_flag"] == 1,
        0.85,
        np.where(predictions["default_flag"] == 1, 0.68, 0.48),
    )
    predictions["exposure_at_default"] = predictions["current_outstanding"].clip(lower=0)
    predictions["model_expected_credit_loss"] = (
        predictions["predicted_default_probability"]
        * predictions["loss_given_default"]
        * predictions["exposure_at_default"]
    ).round(2)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MARTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_FILE)
    metrics.to_csv(METRICS_FILE, index=False)
    feature_importance.to_csv(FEATURE_IMPORTANCE_FILE, index=False)
    predictions.to_csv(PREDICTIONS_FILE, index=False)
    print("Default-risk model trained successfully")
    print(f"Model file: {MODEL_FILE}")
    print(f"Metrics file: {METRICS_FILE}")
    print(f"Feature importance file: {FEATURE_IMPORTANCE_FILE}")
    print(f"Predictions file: {PREDICTIONS_FILE}")
    print("")
    print("Model metrics:")
    print(metrics.to_string(index=False))
    print("")
    print("Top 15 feature importances:")
    print(feature_importance.head(15).to_string(index=False))
    print("")
    print("Prediction risk-band distribution:")
    print(predictions["model_risk_band"].value_counts().to_string())
if __name__ == "__main__":
    train_model()
