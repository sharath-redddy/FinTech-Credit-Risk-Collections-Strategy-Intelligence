import argparse
from pathlib import Path
from google.cloud import bigquery
from src.config import PROCESSED_DATA_DIR
DATASET_NAME = "credit_risk_raw"
TABLE_FILES = {
    "customers_clean": "customers_clean.csv",
    "loan_applications_clean": "loan_applications_clean.csv",
    "loans_clean": "loans_clean.csv",
    "repayment_transactions_clean": "repayment_transactions_clean.csv",
    "delinquency_snapshots_clean": "delinquency_snapshots_clean.csv",
    "collections_actions_clean": "collections_actions_clean.csv",
    "credit_policy_simulations_clean": "credit_policy_simulations_clean.csv",
    "daily_portfolio_metrics_clean": "daily_portfolio_metrics_clean.csv",
}
def create_dataset_if_not_exists(client: bigquery.Client, project_id: str, location: str) -> None:
    dataset_id = f"{project_id}.{DATASET_NAME}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = location
    dataset.description = "Raw clean CSV uploads for CrediSphere credit risk analytics project"
    client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset ready: {dataset_id}")
def load_csv_to_bigquery(
    client: bigquery.Client,
    project_id: str,
    table_name: str,
    csv_path: Path,
) -> None:
    table_id = f"{project_id}.{DATASET_NAME}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with csv_path.open("rb") as source_file:
        load_job = client.load_table_from_file(
            source_file,
            table_id,
            job_config=job_config,
        )
    load_job.result()
    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows:,} rows into {table_id}")
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload processed CrediSphere CSV files to BigQuery."
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="Google Cloud project ID",
    )
    parser.add_argument(
        "--location",
        default="US",
        help="BigQuery dataset location. Default: US",
    )
    args = parser.parse_args()
    client = bigquery.Client(project=args.project_id)
    create_dataset_if_not_exists(
        client=client,
        project_id=args.project_id,
        location=args.location,
    )
    for table_name, file_name in TABLE_FILES.items():
        csv_path = PROCESSED_DATA_DIR / file_name
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Missing processed file: {csv_path}. Run the cleaning step first."
            )
        load_csv_to_bigquery(
            client=client,
            project_id=args.project_id,
            table_name=table_name,
            csv_path=csv_path,
        )
    print("")
    print("All processed datasets uploaded to BigQuery successfully.")
if __name__ == "__main__":
    main()
