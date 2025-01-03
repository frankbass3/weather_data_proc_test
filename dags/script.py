from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
import psycopg2
import pandas as pd
import json
from datetime import datetime
from psycopg2.extras import execute_values
PWD = ""
# Process Weather Data (as you had before)
def process_weather_data(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(task_ids='get_weather_data')  # Pull data from XCom if needed
    
    with open(raw_data, "r") as file:
        test_pwd = file.read()

    weather_data = json.loads(test_pwd.strip())
    processed_data = []
    
    # Process the weather data (your existing logic)
    for record in weather_data['hourly']['data']:
        processed_data.append({
            'latitude' : weather_data["latitude"],
            'longitude' : weather_data["longitude"],
            'timezone' : weather_data["timezone"],
            'offset_data' : weather_data["offset"],
            'elevation' : weather_data["elevation"],
            'current_time_t': datetime.utcfromtimestamp(record['time']),
            'icon': record['icon'],
            'summary': record['summary'],
            'precip_intensity': record['precipIntensity'],
            'precip_accumulation': record['precipAccumulation'],
            'precip_type': record['precipType'],
            'temperature': record['temperature'],
            'apparent_temperature': record['apparentTemperature'],
            'dew_point': record['dewPoint'],
            'pressure': record['pressure'],
            'wind_speed': record['windSpeed'],
            'wind_gust': record['windGust'],
            'wind_bearing': record['windBearing'],
            'cloud_cover': record['cloudCover'],
            'snow_accumulation': record['snowAccumulation']
        })
    
    kwargs['ti'].xcom_push(key='processed_weather_data', value=processed_data)

# Load Weather Data to PostgreSQL (as you had before) comment
def load_weather_data_to_postgresql(**kwargs):
    processed_data = kwargs['ti'].xcom_pull(task_ids='process_weather_data', key='processed_weather_data')
    
    conn_id = "postgres_conn"  # Replace with your connection ID
    conn = BaseHook.get_connection(conn_id)
    
    connection = psycopg2.connect(
        host=conn.host,
        dbname=conn.schema,
        user=conn.login,
        password=conn.password,
        port=conn.port
    )
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO weather_data (
        latitude, longitude, timezone, offset_data, elevation,
        current_time_t, icon, summary, precip_intensity, precip_accumulation,
        precip_type, temperature, apparent_temperature, dew_point, pressure,
        wind_speed, wind_gust, wind_bearing, cloud_cover, snow_accumulation
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (latitude, longitude, current_time_t) DO NOTHING;
    """

    for record in processed_data:
        cursor.execute(insert_query, (
            record['latitude'],
            record['longitude'],
            record['timezone'], 
            record['offset_data'], 
            record['elevation'], 
            record['current_time_t'],
            record['icon'],
            record['summary'],
            record['precip_intensity'],
            record['precip_accumulation'],
            record['precip_type'],
            record['temperature'],
            record['apparent_temperature'],
            record['dew_point'],
            record['pressure'],
            record['wind_speed'],
            record['wind_gust'],
            record['wind_bearing'],
            record['cloud_cover'],
            record['snow_accumulation']
        ))

    connection.commit()
    cursor.close()
    connection.close()


# Function to process the JSONL file and ingest data
def process_jsonl_file_provence(**kwargs):
    jsonl_file_path = kwargs['jsonl_file_path']
    
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            province_data = json.loads(line.strip())
            insert_data_jsonl_provence(province_data)

def insert_data_jsonl_provence(province_data):
    conn_id = "postgres_conn"  # Replace with your connection ID
    conn = BaseHook.get_connection(conn_id)
    
    connection = psycopg2.connect(
        host=conn.host,
        dbname=conn.schema,
        user=conn.login,
        password=conn.password,
        port=conn.port
    )
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO provinces (province_name, province_istat_code, province_boundaries)
            VALUES (%s, %s, ST_GeomFromText(%s, 4326))
        """
        cursor.execute(insert_query, (province_data['province_name'], province_data['province_istat_code'], province_data['province_boundaries']))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def process_jsonl_file_regions(**kwargs):
    jsonl_file_path = kwargs['jsonl_file_path']
    
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            region_data = json.loads(line.strip())
            insert_data_jsonl_regions(region_data)

def insert_data_jsonl_regions(region_data):
    conn_id = "postgres_conn"  # Replace with your connection ID
    conn = BaseHook.get_connection(conn_id)
    
    connection = psycopg2.connect(
        host=conn.host,
        dbname=conn.schema,
        user=conn.login,
        password=conn.password,
        port=conn.port
    )
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO regions (region_name, region_istat, region_boundaries)
            VALUES (%s, %s, ST_GeomFromText(%s, 4326)::polygon)
            ON CONFLICT (region_istat) DO NOTHING;
        """
        cursor.execute(insert_query, (region_data['region_name'], 
                                      region_data['region_istat'], 
                                      region_data['region_boundaries']))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Process CSV Data (as you had before)
def process_csv_data_cities(**kwargs):
    file_path = kwargs['ti'].xcom_pull(task_ids='get_csv_data')  # Pull the file path from XCom if needed
    
    weather_data = pd.read_csv(
        file_path, 
        sep=';',  # Use semicolon as delimiter
        decimal=',',  # Handle European decimal format
    )
    # Convert lat and lon to floats, replacing commas with dots
    weather_data['lat'] = weather_data['lat'].astype(str).str.replace(',', '.').astype(float)
    weather_data['lon'] = weather_data['lon'].astype(str).str.replace(',', '.').astype(float)
    # Convert superficie_kmq to float
    weather_data['superficie_kmq'] = weather_data['superficie_kmq'].astype(str).str.replace(',', '.').astype(float)
    processed_data = weather_data.to_dict(orient='records')  # Convert the DataFrame to a list of dictionaries

    kwargs['ti'].xcom_push(key='processed_csv_data', value=processed_data)

# Load CSV Data to PostgreSQL (as you had before)
def load_csv_data_to_postgresql_cities(**kwargs):
    processed_data = kwargs['ti'].xcom_pull(task_ids='process_csv_data_cities', key='processed_csv_data')
    
    conn_id = "postgres_conn"  # Replace with your connection ID
    conn = BaseHook.get_connection(conn_id)
    
    connection = psycopg2.connect(
        host=conn.host,
        dbname=conn.schema,
        user=conn.login,
        password=conn.password,
        port=conn.port
    )
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO cities (
        sigla_provincia, codice_istat, denominazione_ita_altra, denominazione_ita, 
        denominazione_altra, flag_capoluogo, codice_belfiore, lat, lon, superficie_kmq, codice_sovracomunale
    ) VALUES  %s
    """

    # Prepare data for bulk insertion
    values = [
        (
            record.get('sigla_provincia', ''),
            record.get('codice_istat', ''),
            record.get('denominazione_ita_altra', ''),
            record.get('denominazione_ita', ''),
            record.get('denominazione_altra', ''),
            record.get('flag_capoluogo', ''),
            record.get('codice_belfiore', ''),
            record.get('lat', None),
            record.get('lon', None),
            record.get('superficie_kmq', None),
            record.get('codice_sovracomunale', '')
        )
        for record in processed_data
    ]

    # Define batch size
    BATCH_SIZE = 10000

    # Insert data in batches
    for i in range(0, len(values), BATCH_SIZE):
        execute_values(cursor, insert_query, values[i:i + BATCH_SIZE])

    connection.commit()
    cursor.close()
    connection.close()

with DAG(
    'script_dag_py',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 11, 16),
        'retries': 1,
    },
    description='ETL to process weather data and CSV data and store in PostgreSQL',
    schedule_interval=None,  # Set the schedule interval as needed
) as dag:
    # Task to get weather data  
    get_weather_data = PythonOperator(
        task_id='get_weather_data',
        python_callable=lambda: str(PWD+"ingest/weather/2024-05-22.json"),
    )

    # Task to process weather data
    process_weather_data = PythonOperator(
        task_id='process_weather_data',
        python_callable=process_weather_data,
        provide_context=True,
    )

    # Task to load weather data into PostgreSQL
    load_weather_data_to_postgresql = PythonOperator(
        task_id='load_weather_data_to_postgresql',
        python_callable=load_weather_data_to_postgresql,
        provide_context=True,
    )

    # Task to get CSV data
    get_csv_data = PythonOperator(
        task_id='get_csv_data',
        python_callable=lambda: PWD+'ingest/cities/cities.csv',  # Replace with actual file path
    )

    # Task to process CSV data
    process_csv_data_cities = PythonOperator(
        task_id='process_csv_data_cities',
        python_callable=process_csv_data_cities,
        provide_context=True,
    )

    # Task to load CSV data into PostgreSQL
    load_csv_data_to_postgresql_cities = PythonOperator(
        task_id='load_csv_data_to_postgresql_cities',
        python_callable=load_csv_data_to_postgresql_cities,
        provide_context=True,
    )

    process_jsonl_region = PythonOperator(
        task_id='process_jsonl_region',
        python_callable=process_jsonl_file_regions,
        op_kwargs={'jsonl_file_path': PWD+'ingest/regions/regions.jsonl'},
        dag=dag,
    )

    # Define the task dependencies
    get_weather_data >> process_weather_data >> load_weather_data_to_postgresql
    get_csv_data >> process_csv_data_cities >> load_csv_data_to_postgresql_cities

    process_jsonl_region

    # process_province_jsonl_task = PythonOperator(
    #     task_id='process_province_jsonl',
    #     python_callable=process_jsonl_file_provence,
    #     op_kwargs={'jsonl_file_path': '/path/to/your/province_data.jsonl'},  # Path to your JSONL file
    #     dag=dag,
    # )

    # process_province_jsonl_task

    