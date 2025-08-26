# Fintech ETL Pipeline 🚀

An **ETL pipeline** that processes financial transaction data (CSV → Parquet → S3 → Redshift), built with **PySpark**, **Airflow**, **AWS S3**, and **Amazon Redshift**.

---

## 📂 Project Structure

```
fintech_project/
│── dags/etl_dags.py         # Airflow DAG defining the daily ETL job
│── etl/
│   ├── etl.py                # Main entry point to run ETL
│   ├── extract.py            # Extract module (CSV → DataFrame)
│   ├── transform.py          # Transform module (dim_user, dim_payment, fact_transactions)
│   └── load.py               # Load module (write to S3 + COPY into Redshift)
│── data/transactions_1M.csv  # Sample input data
│── requirements.txt          # Python dependencies
│── docker-compose.yaml       # Launch Airflow with Docker
│── Dockerfile                # Dockerfile for ETL container
│── .env.simple               # Sample environment file (without secrets)
│── .gitignore
```

---

## ⚙️ Setup

### 1. Clone repository
```bash
git clone https://github.com/duc81/fintech-etl.git
cd fintech-etl
```

### 2. Create `.env` file (based on `.env.simple`)
```bash
cp .env.simple .env
```

Edit with your actual AWS and Redshift details:
```env
AWS_REGION=ap-southeast-2
AWS_S3_BUCKET=your-bucket
AWS_S3_PREFIX=dwh
REDSHIFT_HOST=your-redshift-endpoint
REDSHIFT_DB=dev
REDSHIFT_PORT=5439
REDSHIFT_IAM_ROLE_ARN=arn:aws:iam::<account-id>:role/RedshiftS3AccessRole
```

### 3. Install dependencies (local)
```bash
pip install -r requirements.txt
```

### 4. Run ETL locally
```bash
python etl/etl.py
```

---

## 🚀 Airflow Orchestration

Run Airflow using Docker Compose:
```bash
docker compose up -d
```

- Airflow UI: [http://localhost:8080](http://localhost:8080)  
- DAG: `etl_fintech` → trigger to run ETL pipeline.

---

## 📊 Outputs

- **S3**: Partitioned Parquet files for each table (`dim_user`, `dim_payment_method`, `fact_transactions`).  
- **Redshift**: Tables loaded under schema `public`.  

---

## 🛡️ Notes

- `.env.simple` is just a template. Do not commit your real `.env` file.  
- Extendable schema: you can add `dim_time`, `dim_location`, etc. for advanced analysis.  

---

## ✨ Author
👤 **duc81**  
📧 `nduc080199@gmail.com`  
