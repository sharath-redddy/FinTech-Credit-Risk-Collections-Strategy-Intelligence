from pathlib import Path
import pandas as pd
import streamlit as st
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARTS_DIR = PROJECT_ROOT / "data" / "marts"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
STRATEGY_FILE = MARTS_DIR / "mart_credit_risk_strategy.csv"
EXECUTIVE_KPIS_FILE = MARTS_DIR / "mart_executive_kpis.csv"
RISK_ALERTS_FILE = MARTS_DIR / "mart_risk_alerts.csv"
COLLECTIONS_QUEUE_FILE = MARTS_DIR / "mart_collections_work_queue.csv"
POLICY_FILE = PROCESSED_DIR / "credit_policy_simulations_clean.csv"
st.set_page_config(
    page_title="Credit Risk Strategy Assistant",
    page_icon="💳",
    layout="wide",
)
BRIGHT_CSS = """
<style>
    .stApp {
        background: #F8FAFC;
        color: #334155;
    }
    h1, h2, h3 {
        color: #0F172A;
        font-weight: 800;
    }
    .main-title {
        padding: 1.2rem 1.4rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #FFFFFF 0%, #E0F2FE 55%, #DCFCE7 100%);
        border: 1px solid #DCEAF7;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.08);
        margin-bottom: 1.2rem;
    }
    .main-title h1 {
        margin-bottom: 0.25rem;
    }
    .main-title p {
        color: #475569;
        font-size: 1.02rem;
        margin-bottom: 0;
    }
    .metric-card {
        background: #FFFFFF;
        padding: 1rem 1.1rem;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        min-height: 115px;
    }
    .metric-label {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-value {
        color: #0F172A;
        font-size: 1.65rem;
        font-weight: 850;
        margin-top: 0.25rem;
    }
    .metric-note {
        color: #64748B;
        font-size: 0.82rem;
        margin-top: 0.25rem;
    }
    .recommendation-box {
        background: #FFFFFF;
        border-left: 6px solid #2563EB;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }
    .alert-critical {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 6px solid #EF4444;
        padding: 0.9rem 1rem;
        border-radius: 14px;
        margin-bottom: 0.7rem;
    }
    .alert-high {
        background: #FFF7ED;
        border: 1px solid #FED7AA;
        border-left: 6px solid #F97316;
        padding: 0.9rem 1rem;
        border-radius: 14px;
        margin-bottom: 0.7rem;
    }
    .alert-medium {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 6px solid #F59E0B;
        padding: 0.9rem 1rem;
        border-radius: 14px;
        margin-bottom: 0.7rem;
    }
    .section-card {
        background: #FFFFFF;
        padding: 1rem;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }
    .small-muted {
        color: #64748B;
        font-size: 0.9rem;
    }
</style>
"""
def format_inr(value: float) -> str:
    if pd.isna(value):
        return "₹0"
    value = float(value)
    if abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:.2f}Cr"
    if abs(value) >= 100_000:
        return f"₹{value / 100_000:.2f}L"
    return f"₹{value:,.0f}"
def format_pct(value: float) -> str:
    if pd.isna(value):
        return "0.0%"
    return f"{float(value) * 100:.1f}%"
@st.cache_data
def load_data():
    required_files = [
        STRATEGY_FILE,
        EXECUTIVE_KPIS_FILE,
        RISK_ALERTS_FILE,
        COLLECTIONS_QUEUE_FILE,
        POLICY_FILE,
    ]
    missing = [str(file) for file in required_files if not file.exists()]
    if missing:
        return None, missing
    strategy = pd.read_csv(STRATEGY_FILE)
    kpis = pd.read_csv(EXECUTIVE_KPIS_FILE)
    alerts = pd.read_csv(RISK_ALERTS_FILE)
    collections = pd.read_csv(COLLECTIONS_QUEUE_FILE)
    policy = pd.read_csv(POLICY_FILE)
    return {
        "strategy": strategy,
        "kpis": kpis,
        "alerts": alerts,
        "collections": collections,
        "policy": policy,
    }, []
def filter_strategy_data(strategy: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Portfolio Filters")
    loan_products = ["All"] + sorted(strategy["loan_product"].dropna().unique().tolist())
    states = ["All"] + sorted(strategy["state"].dropna().unique().tolist())
    risk_bands = ["All"] + sorted(strategy["risk_band"].dropna().unique().tolist())
    model_risk_bands = ["All"] + ["Low", "Medium", "High", "Critical"]
    delinquency_buckets = ["All"] + sorted(strategy["delinquency_bucket"].dropna().unique().tolist())
    selected_product = st.sidebar.selectbox("Loan Product", loan_products)
    selected_state = st.sidebar.selectbox("State", states)
    selected_risk_band = st.sidebar.selectbox("Underwriting Risk Band", risk_bands)
    selected_model_band = st.sidebar.selectbox("Model Risk Band", model_risk_bands)
    selected_bucket = st.sidebar.selectbox("Delinquency Bucket", delinquency_buckets)
    filtered = strategy.copy()
    if selected_product != "All":
        filtered = filtered[filtered["loan_product"] == selected_product]
    if selected_state != "All":
        filtered = filtered[filtered["state"] == selected_state]
    if selected_risk_band != "All":
        filtered = filtered[filtered["risk_band"] == selected_risk_band]
    if selected_model_band != "All":
        filtered = filtered[filtered["model_risk_band"] == selected_model_band]
    if selected_bucket != "All":
        filtered = filtered[filtered["delinquency_bucket"] == selected_bucket]
    return filtered
def metric_card(label: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
def show_header():
    st.markdown(
        """
        <div class="main-title">
            <h1>Credit Risk Strategy Assistant</h1>
            <p>Bright fintech risk-intelligence app for CrediSphere Finance. Use it to review portfolio health, high-risk loans, expected loss, collections priorities, and policy scenarios.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
def show_kpis(filtered: pd.DataFrame):
    active = filtered[filtered["loan_status"].isin(["Active", "Defaulted"])].copy()
    total_loans = filtered["loan_id"].nunique()
    active_loans = active["loan_id"].nunique()
    outstanding = active["current_outstanding"].sum()
    ecl = active["final_expected_credit_loss"].sum()
    default_rate = filtered["default_flag"].mean() if len(filtered) else 0
    par30 = active["par30_flag"].mean() if len(active) else 0
    par60 = active["par60_flag"].mean() if len(active) else 0
    par90 = active["par90_flag"].mean() if len(active) else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Loans", f"{total_loans:,}", "Filtered portfolio")
    with c2:
        metric_card("Active Loans", f"{active_loans:,}", "Active + defaulted")
    with c3:
        metric_card("Outstanding", format_inr(outstanding), "Current exposure")
    with c4:
        metric_card("Expected Credit Loss", format_inr(ecl), "Model-based ECL")
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        metric_card("Default Rate", format_pct(default_rate), "Historical default flag")
    with c6:
        metric_card("PAR30", format_pct(par30), "30+ days past due")
    with c7:
        metric_card("PAR60", format_pct(par60), "60+ days past due")
    with c8:
        metric_card("PAR90", format_pct(par90), "90+ days past due")
def show_recommendation(filtered: pd.DataFrame):
    active = filtered[filtered["loan_status"].isin(["Active", "Defaulted"])].copy()
    if len(active) == 0:
        recommendation = "No active loans match the selected filters."
    else:
        critical_count = int((active["model_risk_band"] == "Critical").sum())
        high_count = int((active["model_risk_band"] == "High").sum())
        par30_rate = active["par30_flag"].mean()
        total_ecl = active["final_expected_credit_loss"].sum()
        if critical_count > 0 and par30_rate >= 0.20:
            recommendation = (
                f"Prioritize collections and monitoring. This filtered portfolio has {critical_count:,} Critical loans, "
                f"{high_count:,} High-risk loans, PAR30 of {format_pct(par30_rate)}, and ECL of {format_inr(total_ecl)}."
            )
        elif high_count > 0:
            recommendation = (
                f"Use early warning monitoring for High-risk loans. Current filtered ECL is {format_inr(total_ecl)}."
            )
        else:
            recommendation = (
                f"Portfolio segment looks relatively stable. Continue monitoring PAR movement and ECL trends."
            )
    st.markdown(
        f"""
        <div class="recommendation-box">
            <h3>Strategy Recommendation</h3>
            <p>{recommendation}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
def show_alerts(alerts: pd.DataFrame):
    st.subheader("Risk Alerts")
    for _, row in alerts.iterrows():
        severity = str(row["severity"]).lower()
        if severity == "critical":
            css_class = "alert-critical"
        elif severity == "high":
            css_class = "alert-high"
        else:
            css_class = "alert-medium"
        st.markdown(
            f"""
            <div class="{css_class}">
                <b>{row['alert_type']} · {row['severity']}</b><br>
                {row['alert_message']}<br>
                <span class="small-muted">Recommended action: {row['recommended_action']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
def show_top_risky_loans(filtered: pd.DataFrame):
    st.subheader("Top High-Risk Loans")
    columns = [
        "risk_rank",
        "loan_id",
        "state",
        "loan_product",
        "model_risk_band",
        "delinquency_bucket",
        "current_outstanding",
        "predicted_default_probability",
        "final_expected_credit_loss",
        "recommended_strategy_action",
    ]
    available_columns = [col for col in columns if col in filtered.columns]
    top_loans = filtered.sort_values("final_expected_credit_loss", ascending=False).head(25)[available_columns].copy()
    if "current_outstanding" in top_loans.columns:
        top_loans["current_outstanding"] = top_loans["current_outstanding"].round(2)
    if "final_expected_credit_loss" in top_loans.columns:
        top_loans["final_expected_credit_loss"] = top_loans["final_expected_credit_loss"].round(2)
    if "predicted_default_probability" in top_loans.columns:
        top_loans["predicted_default_probability"] = (top_loans["predicted_default_probability"] * 100).round(2)
    st.dataframe(top_loans, use_container_width=True, hide_index=True)
def show_collections_queue(collections: pd.DataFrame, filtered: pd.DataFrame):
    st.subheader("Collections Priority Work Queue")
    valid_loans = set(filtered["loan_id"].unique())
    queue = collections[collections["loan_id"].isin(valid_loans)].copy()
    if len(queue) == 0:
        st.info("No collection queue records match the selected filters.")
        return
    columns = [
        "loan_id",
        "state",
        "loan_product",
        "model_risk_band",
        "delinquency_bucket",
        "days_past_due",
        "current_outstanding",
        "collections_priority_score",
        "expected_recoverable_value",
        "recommended_next_action",
        "total_contact_attempts",
        "promise_to_pay_count",
        "last_action_date",
    ]
    available_columns = [col for col in columns if col in queue.columns]
    queue = queue.sort_values("collections_priority_score", ascending=False).head(30)
    st.dataframe(queue[available_columns], use_container_width=True, hide_index=True)
def show_policy_simulator(policy: pd.DataFrame):
    st.subheader("Credit Policy Scenario Simulator")
    policy_view = policy.copy()
    policy_view["predicted_approval_rate"] = (policy_view["predicted_approval_rate"] * 100).round(2)
    policy_view["predicted_default_rate"] = (policy_view["predicted_default_rate"] * 100).round(2)
    policy_view["profit_after_expected_loss"] = (
        policy_view["projected_revenue"] - policy_view["expected_credit_loss"]
    ).round(2)
    columns = [
        "policy_name",
        "minimum_credit_score",
        "maximum_debt_to_income_ratio",
        "maximum_loan_to_income_ratio",
        "predicted_approval_rate",
        "predicted_default_rate",
        "expected_credit_loss",
        "projected_revenue",
        "profit_after_expected_loss",
        "policy_recommendation",
    ]
    st.dataframe(policy_view[columns], use_container_width=True, hide_index=True)
    recommended = policy_view[
        policy_view["policy_recommendation"].str.contains("Recommended", case=False, na=False)
    ]
    if len(recommended) > 0:
        row = recommended.iloc[0]
        st.success(
            f"Recommended policy: {row['policy_name']} | Approval Rate: {row['predicted_approval_rate']}% | Default Rate: {row['predicted_default_rate']}%"
        )
def show_responsible_lending_note():
    st.subheader("Responsible Lending Note")
    st.info(
        "This app uses synthetic data only. Fairness or disparity signals in this project are for portfolio demonstration and monitoring practice, not evidence of real-world bias. Sensitive attributes should not be used as direct approval rules."
    )
def main():
    st.markdown(BRIGHT_CSS, unsafe_allow_html=True)
    show_header()
    data, missing = load_data()
    if missing:
        st.error("Required mart files are missing. Run the project pipeline first:")
        st.code("python -m src.pipeline.run_full_pipeline")
        st.write("Missing files:")
        for file in missing:
            st.write(f"- {file}")
        return
    strategy = data["strategy"]
    alerts = data["alerts"]
    collections = data["collections"]
    policy = data["policy"]
    filtered = filter_strategy_data(strategy)
    show_kpis(filtered)
    show_recommendation(filtered)
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Risk Alerts",
            "High-Risk Loans",
            "Collections Queue",
            "Policy Simulator",
        ]
    )
    with tab1:
        show_alerts(alerts)
        show_responsible_lending_note()
    with tab2:
        show_top_risky_loans(filtered)
    with tab3:
        show_collections_queue(collections, filtered)
    with tab4:
        show_policy_simulator(policy)
if __name__ == "__main__":
    main()
