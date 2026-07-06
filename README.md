# Azure Data Engineering Pipeline
### SQL Server → ADF → ADLS Gen2 → Databricks → Unity Catalog → Power BI

An end-to-end data engineering project built on Microsoft Azure, implementing a full medallion architecture (Bronze → Silver → Gold) using industry-standard tools and practices.

Built as part of an Industrial Training placement under a Data Platform Engineering Lead in a Data Architecture & Engineering department.

---

## Architecture Overview

```
Azure SQL Database          (Source — structured relational data)
        ↓
Azure Data Factory          (Ingestion — Copy pipelines, orchestration)
        ↓
Azure Data Lake Gen2        (Landing / Bronze layer — raw files)
        ↓
Azure Databricks + PySpark  (Transformation — cleaning, enrichment)
        ↓
Unity Catalog Tables        (Silver / Gold layers — governed, queryable)
        ↓
Power BI                    (Reporting — dashboards and visualizations)
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Azure SQL Database | Source system — relational tables |
| Azure Data Factory (ADF) | Pipeline orchestration and data ingestion |
| Azure Data Lake Storage Gen2 (ADLS Gen2) | Raw data storage (Bronze layer) |
| Azure Databricks | Data transformation using PySpark |
| Unity Catalog | Data governance, lineage, access control |
| Power BI | Business intelligence and reporting |
| PySpark | Distributed data processing language |

---

## Project Phases

### ✅ Phase 1 — Azure SQL Database Setup
- Created Azure SQL Database and server (East Asia region)
- Configured networking — enabled Azure services access and client IP firewall rules
- Resolved region-restriction issue via Azure Policy allowed-regions check

### ✅ Phase 2 — Source Tables and Sample Data
- Created three related tables: `Customers`, `Products`, `Orders`
- Defined foreign key relationships between tables
- Inserted sample data (10 customers, 10 products, 15 orders)
- Verified data integrity with JOIN queries across all three tables

### ✅ Phase 3 — ADF Ingestion into ADLS Gen2
- Created ADLS Gen2 storage account with hierarchical namespace enabled
- Set up `landing` container as the Bronze/raw data layer
- Created Azure Data Factory instance
- Built Linked Services connecting ADF to both SQL Database and ADLS Gen2
- Deployed a Copy Data pipeline (`CopySQLtoLake`) with one activity per table, each using its own explicit SQL dataset and ADLS sink dataset
- All three tables (`Customers`, `Products`, `Orders`) verified landing correctly as delimited text files in `landing/customers/`, `landing/products/`, `landing/orders/`
- Resolved real issues along the way: an expired storage account key causing authentication failures, and incorrect dataset path/schema configuration during initial setup

### ✅ Phase 4 — Databricks Transformation + Unity Catalog
- Set up Azure Databricks workspace (Premium tier, serverless compute)
- Connected ADLS Gen2 to Unity Catalog via Access Connector (managed identity) and External Location — verified read/write/list/delete access
- PySpark script (`01_customer_transform.py`): read raw customer CSV → added derived `FullName` column → wrote result as Parquet → read Parquet back and wrote a cleaned CSV to a separate `processed/` folder
- Created a dedicated Unity Catalog schema (`customer_data`) for the project
- PySpark script (`02_unity_catalog_work.py`):
  - Read cleaned customer CSV and wrote it into a managed Unity Catalog table (`customers_bronze`)
  - Re-read the source data, added a derived `IsMetro` column, and wrote it into a second managed table (`customers_enriched`)
  - Created a Unity Catalog **view** (`metro_customers_view`) filtering enriched customers to metro cities only
  - Created a Unity Catalog **SQL function** (`classify_signup`) categorizing customers as "Recent" or "Older" based on signup date, called directly within a query

### ✅ Phase 5 — Further Cleaning and Gold Layer
- Read the Silver-layer table (`customers_enriched`) directly from Unity Catalog by table name
- Built an aggregated, business-ready summary — customer counts grouped by City and metro classification (`IsMetro`)
- Wrote the result into a new Gold-layer Unity Catalog table (`customers_gold_summary`)

### ✅ Phase 6 — Power BI Report
- Connected Power BI Desktop to Unity Catalog via a Databricks SQL Warehouse (Personal Access Token authentication)
- Loaded the Gold-layer table (`customers_gold_summary`) directly into Power BI
- Built a bar chart visualizing customer distribution by city, split by metro classification
- Full traceability confirmed: every value on the report traces back to a row originally inserted in Azure SQL Database in Phase 2

---

## Repository Structure

```
├── README.md
├── notebooks/
│   ├── 01_customer_transform.py     # Bronze layer: raw read + FullName enrichment + Parquet round-trip
│   ├── 02_unity_catalog_work.py     # Silver layer: UC tables, view, and function
│   └── 03_gold_layer_transform.py   # Gold layer: aggregated summary table
├── adf-pipelines/
│   └── CopySQLtoLake.json           # ADF pipeline definition
├── sql/
│   └── create_tables.sql            # Source table DDL and sample data
└── powerbi/
    ├── customer_analytics.pbix      # Power BI report on Gold-layer data
    └── powerbi_report_screenshot.png
```

---

## Key Concepts Implemented

- **Medallion Architecture** — Bronze (raw landing) → Silver (cleaned) → Gold (aggregated)
- **ETL vs ELT** — ADF handles E and L; Databricks handles T
- **Schema-on-read** — raw data lands in the lake without enforced structure; schema is applied at read time in Databricks
- **Data Governance** — Unity Catalog provides centralized access control, data lineage, and discoverability
- **Managed Identity Authentication** — Access Connector used instead of raw storage keys for secure, credential-free storage access

---

## Setup Guide

> Pre-requisites: Active Azure subscription, Power BI Desktop installed

1. **SQL Database** — Run `sql/create_tables.sql` against a new Azure SQL Database to recreate the source tables and sample data
2. **Storage** — Create an ADLS Gen2 storage account with hierarchical namespace enabled; create a `landing` container
3. **ADF** — Import `adf-pipelines/CopySQLtoLake.json` into a new Azure Data Factory instance; update Linked Service connection strings to point to your resources
4. **Databricks** — Create an Azure Databricks workspace; import the `.py` files from the `notebooks/` folder as source-linked notebooks; update the storage account path in the first cell to match your setup
5. **Unity Catalog** — Set up an Access Connector and External Location pointing to your ADLS Gen2 container (see notebook comments for details)

---

## Author

**Rahul Varma** — Final Year B.Tech Information Technology, MIT Manipal  
ITR Project | Data Architecture & Engineering Department  
[LinkedIn](https://www.linkedin.com/in/dhanunjay-rahul-varma-646893270/) <!-- add your LinkedIn URL here -->

---

*Project in progress — updated as each phase is completed.*
