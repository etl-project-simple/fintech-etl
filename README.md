# Fintech ETL Pipeline 🚀

An **ETL pipeline** that processes financial transaction data (CSV → Parquet → S3 → Redshift), built with **PySpark**, **Airflow**, **AWS S3**, and **Amazon Redshift**.

---

## 📂 Project Structure

```
fintech_project/
│── dags/etl_dags.py         # Airflow DAG defining the daily ETL job
│── etl/
│   ├── main.py               # Main entry point to run ETL
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
git clone https://github.com/etl-project-simple/fintech-etl.git
cd fintech-etl
```

### 2. Create `.env` file (based on `.env.simple`)
```bash
cp .env.simple .env
```

### 3. Install dependencies (local)
```bash
pip install -r requirements.txt
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

## 🏗️ Pipeline Architecture

```
Raw CSV → PySpark (Extract + Transform) → 
S3 (Parquet, partitioned) → 
Amazon Redshift (Fact & Dimension tables) → 
Analytics / BI
```

![ETL Pipeline Diagram](docs/etl_pipeline.png)

---

## 📈 Demo Results

After running the ETL pipeline on **transactions_1M.csv**, the data is transformed into the following tables:

- **dim_user**
  | user_id | total_transactions | total_amount  | average_amount |  last_transaction   |
  |---------|--------------------|---------------|----------------|---------------------|
  | 1       | 14                 | 30,361,020.97 | 2,168,644.35   | 2025-01-30 09:46:54 |
  | 2       | 13                 | 40,415,737.05 | 3,108,903.62   | 2025-01-27 21:15:36 |
  | 3       | 9                  | 20,025,137.80 | 2,225,015.31   | 2025-01-25 10:45:36 |
  | 4       | 13                 | 34,236,665.75 | 2,633,590.06   | 2025-01-28 09:28:41 |
  | 5       | 9                  | 28,035,589.30 | 3,115,065.48   | 2025-01-30 12:30:15 |

- **dim_payment_method**
  | payment_method | total_transactions |  total_amount   | average_amount |
  |----------------|--------------------|-----------------|----------------|
  | Bank Transfer  | 200,121            | 501,543,600,000 | 2,506,202.0    |
  | Credit Card    | 200,022            | 499,590,400,000 | 2,497,677.0    |
  | Momo           | 199,999            | 500,750,800,000 | 2,503,766.0    |
  | VNPay          | 199,829            | 498,936,300,000 | 2,496,816.0    |
  | ZaloPay        | 200,029            | 499,384,800,000 | 2,496,562.0    |

- **fact_transactions**
  | transaction_date | payment_method | total_transactions |  total_amount  | average_amount |
  |------------------|----------------|--------------------|----------------|----------------|
  | 2025-01-01       | Bank Transfer  | 6,514              | 16,460,700,000 | 2,526,973.0    |
  | 2025-01-01       | Credit Card    | 6,709              | 16,831,080,000 | 2,508,731.0    |
  | 2025-01-01       | Momo           | 6,544              | 16,377,440,000 | 2,502,665.0    |
  | 2025-01-01       | VNPay          | 6,693              | 16,720,520,000 | 2,498,210.0    |
  | 2025-01-01       | ZaloPay        | 6,552              | 16,117,520,000 | 2,459,939.0    |

---

## 📊 Outputs

- **S3**: Partitioned Parquet files for each table (`dim_user`, `dim_payment_method`, `fact_transactions`).  
- **Redshift**: Tables loaded under schema `public`.  

You can query results with SQL:

```sql
SELECT * FROM public.dim_user LIMIT 10;
SELECT * FROM public.dim_payment_method LIMIT 10;
SELECT * FROM public.fact_transactions ORDER BY transaction_date DESC LIMIT 10;
```

---

## 🛡️ Notes

- `.env.simple` is just a template. Do not commit your real `.env` file.  
- Extendable schema: you can add `dim_time`, `dim_location`, etc. for advanced analysis.  

---

## ✨ Author
👤 **duc81**  
📧 `nduc080199@gmail.com`  
