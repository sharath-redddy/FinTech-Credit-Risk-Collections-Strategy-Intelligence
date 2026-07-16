# Run Guide
## 1. Create Virtual Environment
python -m venv .venv
## 2. Activate Virtual Environment
PowerShell:
.\.venv\Scripts\Activate.ps1
If scripts are blocked:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
## 3. Install Requirements
pip install -r requirements.txt
## 4. Run Full Pipeline
python -m src.pipeline.run_full_pipeline
## 5. Key Local Outputs
Generated raw data:
data/raw
Cleaned data:
data/processed
Analytics marts:
data/marts
Reports:
outputs/reports
Model:
models/default_risk_model.pkl
## 6. BigQuery Upload
Use this only after Google Cloud authentication is configured:
python -m src.warehouse.load_processed_data_to_bigquery --project-id YOUR_GCP_PROJECT_ID --location US
## 7. Streamlit App
Run after the marts are generated:
streamlit run streamlit_app/app.py
## 8. Power BI
Power BI dashboard should be built separately using the final marts from data/marts.
