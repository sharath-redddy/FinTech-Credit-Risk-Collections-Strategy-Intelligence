import random
from datetime import timedelta
import numpy as np
import pandas as pd
from src.config import (
    DELINQUENCY_SNAPSHOTS_FILE,
    LOANS_FILE,
    COLLECTIONS_ACTIONS_FILE,
    RANDOM_SEED,
)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
CHANNEL_BY_BUCKET = {
    "1-30 DPD": ["SMS", "WhatsApp", "Email", "Phone Call"],
    "31-60 DPD": ["Phone Call", "WhatsApp", "Email", "SMS"],
    "61-90 DPD": ["Phone Call", "Field Follow-up", "WhatsApp", "Email"],
    "90+ DPD": ["Settlement Desk", "Field Follow-up", "Phone Call", "Legal Notice"],
    "Default": ["Settlement Desk", "Recovery Agency", "Legal Notice", "Field Follow-up"],
    "Write-off": ["Recovery Agency", "Settlement Desk", "Legal Notice"],
}
ACTION_TYPE_BY_BUCKET = {
    "1-30 DPD": ["Reminder", "Soft Reminder", "Payment Link Sent"],
    "31-60 DPD": ["Call", "Reminder", "Escalation"],
    "61-90 DPD": ["Escalation", "Field Follow-up", "Settlement Offer"],
    "90+ DPD": ["Settlement Offer", "Legal Review", "Field Follow-up"],
    "Default": ["Settlement Offer", "Legal Review", "Recovery Agency Assignment"],
    "Write-off": ["Legal Review", "Settlement Offer", "Recovery Agency Assignment"],
}
AGENTS = [f"AGENT{i:03d}" for i in range(1, 61)]
AGENT_SKILL = {
    agent: np.random.uniform(0.75, 1.25)
    for agent in AGENTS
}
def should_create_action(bucket: str) -> bool:
    probabilities = {
        "1-30 DPD": 0.45,
        "31-60 DPD": 0.68,
        "61-90 DPD": 0.82,
        "90+ DPD": 0.88,
        "Default": 0.80,
        "Write-off": 0.55,
    }
    return np.random.random() < probabilities.get(bucket, 0.0)
def choose_attempts(bucket: str) -> int:
    if bucket == "1-30 DPD":
        return random.choices([1, 2], weights=[0.82, 0.18], k=1)[0]
    if bucket == "31-60 DPD":
        return random.choices([1, 2, 3], weights=[0.55, 0.34, 0.11], k=1)[0]
    if bucket == "61-90 DPD":
        return random.choices([1, 2, 3], weights=[0.42, 0.38, 0.20], k=1)[0]
    if bucket in ["90+ DPD", "Default"]:
        return random.choices([1, 2, 3, 4], weights=[0.35, 0.34, 0.21, 0.10], k=1)[0]
    return random.choices([1, 2], weights=[0.70, 0.30], k=1)[0]
def choose_channel(bucket: str) -> str:
    channel_weights = {
        "1-30 DPD": [0.36, 0.34, 0.16, 0.14],
        "31-60 DPD": [0.42, 0.28, 0.16, 0.14],
        "61-90 DPD": [0.42, 0.25, 0.22, 0.11],
        "90+ DPD": [0.35, 0.25, 0.25, 0.15],
        "Default": [0.36, 0.27, 0.22, 0.15],
        "Write-off": [0.45, 0.35, 0.20],
    }
    channels = CHANNEL_BY_BUCKET[bucket]
    weights = channel_weights[bucket]
    return random.choices(channels, weights=weights, k=1)[0]
def choose_action_type(bucket: str) -> str:
    return random.choice(ACTION_TYPE_BY_BUCKET[bucket])
def promise_probability(bucket: str, channel: str, attempt_number: int) -> float:
    base = {
        "1-30 DPD": 0.30,
        "31-60 DPD": 0.27,
        "61-90 DPD": 0.22,
        "90+ DPD": 0.17,
        "Default": 0.13,
        "Write-off": 0.07,
    }.get(bucket, 0.10)
    if channel in ["WhatsApp", "Phone Call"]:
        base += 0.05
    if channel in ["Legal Notice", "Recovery Agency"]:
        base -= 0.03
    if attempt_number >= 3:
        base -= 0.04
    return max(0.02, min(base, 0.45))
def recovery_probability(bucket: str, promise_to_pay_flag: int, channel: str, agent_skill: float) -> float:
    base = {
        "1-30 DPD": 0.32,
        "31-60 DPD": 0.25,
        "61-90 DPD": 0.18,
        "90+ DPD": 0.12,
        "Default": 0.08,
        "Write-off": 0.04,
    }.get(bucket, 0.05)
    if promise_to_pay_flag == 1:
        base += 0.18
    if channel in ["Phone Call", "WhatsApp", "Settlement Desk"]:
        base += 0.04
    if channel in ["Legal Notice", "Recovery Agency"]:
        base -= 0.02
    base *= agent_skill
    return max(0.01, min(base, 0.65))
def recovered_amount(bucket: str, outstanding_balance: float, recovered: bool) -> float:
    if not recovered:
        return 0.0
    recovery_fraction_ranges = {
        "1-30 DPD": (0.12, 0.45),
        "31-60 DPD": (0.08, 0.35),
        "61-90 DPD": (0.05, 0.25),
        "90+ DPD": (0.03, 0.18),
        "Default": (0.02, 0.13),
        "Write-off": (0.01, 0.08),
    }
    low, high = recovery_fraction_ranges.get(bucket, (0.01, 0.10))
    amount = outstanding_balance * np.random.uniform(low, high)
    return round(float(max(0, min(amount, outstanding_balance))), 2)
def choose_outcome(promise_to_pay_flag: int, recovered_amount_value: float, bucket: str) -> str:
    if recovered_amount_value > 0:
        if bucket in ["Default", "Write-off", "90+ DPD"]:
            return random.choices(
                ["Partial Recovery", "Settlement Accepted", "Paid"],
                weights=[0.58, 0.30, 0.12],
                k=1,
            )[0]
        return random.choices(
            ["Paid", "Partial Recovery", "Promise Kept"],
            weights=[0.45, 0.35, 0.20],
            k=1,
        )[0]
    if promise_to_pay_flag == 1:
        return random.choice(["Promise to Pay", "Promise Pending"])
    return random.choices(
        ["No Response", "Contacted No Payment", "Wrong Time", "Escalated"],
        weights=[0.38, 0.31, 0.16, 0.15],
        k=1,
    )[0]
def generate_collections_actions() -> pd.DataFrame:
    if not DELINQUENCY_SNAPSHOTS_FILE.exists():
        raise FileNotFoundError(f"Missing file: {DELINQUENCY_SNAPSHOTS_FILE}")
    if not LOANS_FILE.exists():
        raise FileNotFoundError(f"Missing file: {LOANS_FILE}")
    snapshots = pd.read_csv(DELINQUENCY_SNAPSHOTS_FILE)
    loans = pd.read_csv(LOANS_FILE)
    delinquent = snapshots[
        snapshots["delinquency_bucket"].isin(
            ["1-30 DPD", "31-60 DPD", "61-90 DPD", "90+ DPD", "Default", "Write-off"]
        )
    ].copy()
    delinquent["snapshot_date"] = pd.to_datetime(delinquent["snapshot_date"])
    delinquent = delinquent.sort_values(["loan_id", "snapshot_date"])
    valid_loan_ids = set(loans["loan_id"].unique())
    actions = []
    action_counter = 1
    loan_attempt_counter = {}
    for _, row in delinquent.iterrows():
        loan_id = row["loan_id"]
        if loan_id not in valid_loan_ids:
            continue
        bucket = row["delinquency_bucket"]
        if not should_create_action(bucket):
            continue
        attempts = choose_attempts(bucket)
        for _ in range(attempts):
            current_attempt = loan_attempt_counter.get(loan_id, 0) + 1
            loan_attempt_counter[loan_id] = current_attempt
            action_date = row["snapshot_date"] - timedelta(days=random.randint(0, 24))
            channel = choose_channel(bucket)
            action_type = choose_action_type(bucket)
            agent_id = random.choice(AGENTS)
            agent_skill = AGENT_SKILL[agent_id]
            p2p_prob = promise_probability(
                bucket=bucket,
                channel=channel,
                attempt_number=current_attempt,
            )
            promise_to_pay_flag = int(np.random.random() < p2p_prob)
            rec_prob = recovery_probability(
                bucket=bucket,
                promise_to_pay_flag=promise_to_pay_flag,
                channel=channel,
                agent_skill=agent_skill,
            )
            is_recovered = np.random.random() < rec_prob
            recovery_value = recovered_amount(
                bucket=bucket,
                outstanding_balance=float(row["outstanding_balance"]),
                recovered=is_recovered,
            )
            outcome = choose_outcome(
                promise_to_pay_flag=promise_to_pay_flag,
                recovered_amount_value=recovery_value,
                bucket=bucket,
            )
            actions.append(
                {
                    "action_id": f"ACT{action_counter:09d}",
                    "loan_id": loan_id,
                    "customer_id": row["customer_id"],
                    "action_date": action_date.date(),
                    "collection_channel": channel,
                    "agent_id": agent_id,
                    "action_type": action_type,
                    "promise_to_pay_flag": promise_to_pay_flag,
                    "recovered_amount": recovery_value,
                    "action_outcome": outcome,
                    "contact_attempt_number": current_attempt,
                }
            )
            action_counter += 1
    actions_df = pd.DataFrame(actions)
    if len(actions_df) > 0:
        missing_agent_idx = actions_df.sample(frac=0.003, random_state=RANDOM_SEED + 501).index
        actions_df.loc[missing_agent_idx, "agent_id"] = np.nan
    return actions_df
def main() -> None:
    actions = generate_collections_actions()
    COLLECTIONS_ACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    actions.to_csv(COLLECTIONS_ACTIONS_FILE, index=False)
    print("collections_actions.csv generated successfully")
    print(f"Output file: {COLLECTIONS_ACTIONS_FILE}")
    print(f"Rows: {len(actions):,}")
    print(f"Columns: {actions.shape[1]}")
    print("")
    print("Collection channel distribution:")
    print(actions["collection_channel"].value_counts().to_string())
    print("")
    print("Action outcome distribution:")
    print(actions["action_outcome"].value_counts().to_string())
    print("")
    print("Recovered amount summary:")
    print(actions["recovered_amount"].describe().round(2).to_string())
    print("")
    print("Sample records:")
    print(actions.head(5).to_string(index=False))
if __name__ == "__main__":
    main()
