from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils.dates import days_ago
import pandas as pd
import os

def export_data_from_mysql():
    hook = MySqlHook(mysql_conn_id='mysql_conn')
    engine = hook.get_sqlalchemy_engine()
    df = pd.read_sql('SELECT * FROM tugas', con=engine)
    local_path = '/opt/airflow/datasource/datasource.csv'
    df.to_csv(local_path, index=False)
    return local_path

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'data_transfer_to_gcs',
    default_args=default_args,
    description='DAG untuk mengekspor data dari MySQL dan mengunggah ke GCS',
    schedule_interval='@once',
    start_date=days_ago(1),
) as dag:

    export_data_task = PythonOperator(
        task_id='export_data_from_mysql',
        python_callable=export_data_from_mysql,
    )

    upload_to_gcs_task = LocalFilesystemToGCSOperator(
        task_id='upload_to_gcs',
        src="{{ task_instance.xcom_pull(task_ids='export_data_from_mysql') }}",
        dst='testing2/data-source.csv',
        bucket='testing-de',
        gcp_conn_id='google_cloud_default',  # Gunakan nama koneksi GCS yang benar
    )

    export_data_task >> upload_to_gcs_task
