# Project Testing: Sample Data Ingestion in PostgreSQL with Airflow, Python, and GitHub Actions

This repository contains scripts to set up a PostgreSQL database and an Apache Airflow environment on a provisioned machine. Follow the steps below for the configuration.

---

## Prerequisites

1. **Provisioned Machine:** Ensure you have a machine provisioned and ready for use. If not, you can use the Terraform script in the `terraform` folder. See the **Notes** section for more details.  
2. **Execution Permissions:** Grant execution roles to the following scripts:
   - `setup_postgres.sh`
   - `setup_airflow.sh`
3. **Networking:**
   - If PostgreSQL and Airflow are hosted on separate machines, ensure PostgreSQL's port (default: 5432) is open for external connections.
   - If they are in different VPCs, a VPC peering connection and proper routing must be set up.
4. **Airflow Setup:** Connect to the Airflow user interface and configure the connection to the PostgreSQL database.
5. **Data Hypothesis:**
   - The following files are expected to arrive in the VM already uncompressed:
     - `cities` as CSV
     - `regions` as JSONL
     - `provinces` as JSONL
     - `weather` as JSON
   - These files should be located in directory /ingest and the following sub-directories:
     - `/cities`
     - `/regions`
     - `/provinces`
     - `/weather`
   - The `cities`, `regions`, and `provinces` data do not change frequently, so they will be fully overwritten. These datasets are relatively small.

---

## Installation Steps

### Step 1: Run the Setup Scripts on the VM

1. Execute the following scripts in the specified order:
   - First, run:  
     ```bash
     ./setup_postgres.sh
     ```
   - Then, run:  
     ```bash
     ./setup_airflow.sh
     ```
   - Then execute the script setup_db.sql in your posrgresql database for create the tables
   ```bash
      setup_db.sql
   ```

### Step 2: In case of configure PostgreSQL on the VM for allows external connections

1. Edit PostgreSQL's configuration file to allow external connections:  
   ```bash
   sudo nano /etc/postgresql/16/main/postgresql.conf

   Update the following line:

   listen_addresses = '*'
   
   Update PostgreSQLs authentication configuration

   sudo nano /etc/postgresql/16/main/pg_hba.conf

   Add the following line

   host    all    all    0.0.0.0/0    md5

2. Restart postgresql 
   ```bash

   sudo systemctl restart postgresql

## Deployment Instructions

1. Push your code to this repository on GitHub. The GitHub Actions workflow has been configured (with secrets), and actions will run on every push to automatically copy the DAG to the Airflow machine.  
2. The **GitHub Actions** workflow will automatically trigger deployment and execute the `script.py` file within Airflow.

---

## Notes
1. To run a VM, the script uses AWS Cloud, and for this, you can use the Terraform script in the `/Terraform` folder.  
You need to run:
```bash

terraform init
terraform plan
terraform apply
```

2. Ensure all security group or firewall rules are configured properly for network connections.
3. Test the connectivity between the PostgreSQL database and Airflow to validate the setup.

