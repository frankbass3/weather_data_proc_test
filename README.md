# Project Setup: PostgreSQL and Airflow Configuration

This repository provides scripts to set up a PostgreSQL database and an Apache Airflow environment on a provisioned machine. Follow the steps below for the configuration.

---

## Prerequisites

1. **Provisioned Machine:** Ensure you have a machine provisioned and ready for use.  
2. **Execution Permissions:** Grant execution roles to the following scripts:
   - `setup_postgres.sh`
   - `setup_airflow.sh`
3. **Networking:** If PostgreSQL and Airflow are hosted on separate machines, ensure the following:
   - PostgreSQL's port (default: 5432) is open for external connections.
   - Machines on different VPCs require a VPC peering connection and proper routing.
4. **Setup Airflow** Connecto to airflow user interface and setup the connection to the postgresql db
5. **Hypotesis:** The following:
   - The files cities, regions, provinces, weather arrives inside the VM already in 
uncompressed format: cities as csv, regions as jsonl, provinces as jsonl, weather as json.
   - They are in 4 different folders: /cities, /regions, /provinces, /weather
   - The cities, regions and provinces do not change so they are in full overwrite also because they are a few amount of data. 

---

## Installation Steps

### Step 1: Run the Setup Scripts into the VM

1. Execute the following scripts in the specified order:
   - First, run:  
     ```bash
     ./setup_postgres.sh
     ```
   - Next, run:  
     ```bash
     ./setup_airflow.sh
     ```

### Step 2: Configure PostgreSQL into the VM

1. Edit PostgreSQL's configuration file to allow connections:  
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

3. Execute the script setup_db.sql in your posrgresql database

## Deployment Instructions

1. Push your code to this repository.  
2. The **GitHub Actions** workflow will automatically trigger deployment and execute the `script.py` file within Airflow.

---

## Notes
- Ensure all security group or firewall rules are configured properly for network connections.
- Test the connectivity between the PostgreSQL database and Airflow to validate the setup.

