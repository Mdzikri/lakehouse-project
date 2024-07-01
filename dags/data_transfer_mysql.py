from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine

def load_data_to_mysql():
    # conections
    hook = MySqlHook(mysql_conn_id='mysql_conn2')
    engine = create_engine(hook.get_uri())
    #read data
    df = pd.read_csv('/opt/airflow/csv/online_gaming_behavior_dataset.csv')
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
    schedule_interval='0 17 * * *',
    start_date=datetime.today()
)

transfer_data = PythonOperator(
    task_id='load_data_to_mysql',
    python_callable=load_data_to_mysql,
    dag=dag,
)

transfer_data
