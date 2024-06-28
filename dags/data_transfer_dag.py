from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine

def load_data_to_mysql():
    # Gunakan MySqlHook untuk mendapatkan koneksi dari UI Airflow
    hook = MySqlHook(mysql_conn_id='mysql_conn')
    engine = create_engine(hook.get_uri())
    # Baca dataset
    df = pd.read_csv('/opt/airflow/dags/data/online_gaming_behavior_dataset.csv')
    # Masukkan data ke tabel MySQL
    df.to_sql('tugas', con=engine, if_exists='replace', index=False)

dag = DAG(
    'data_transfer_to_mysql',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
    },
    description='A simple DAG to transfer data to MySQL',
    schedule_interval='@once',
    start_date=days_ago(1),
)

transfer_data = PythonOperator(
    task_id='load_data_to_mysql',
    python_callable=load_data_to_mysql,
    dag=dag,
)

transfer_data
