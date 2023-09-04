from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from main_functions import train_cancellations, train_demand, predict

default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


# Define the DAG for the train_cancellations module
train_cancellations_dag = DAG(
    'train_cancellations_dag',
    schedule_interval='@weekly',
    default_args=default_args,
    catchup=False
)

train_cancellations_task = PythonOperator(
    task_id='train_cancellations_task',
    python_callable=train_cancellations,
    dag=train_cancellations_dag
)

# Define the DAG for the train_demand module
train_demand_dag = DAG(
    'train_demand_dag',
    schedule_interval='@monthly',
    default_args=default_args,
    catchup=False
)

train_demand_task = PythonOperator(
    task_id='train_demand_task',
    python_callable=train_demand,
    dag=train_demand_dag
)

# Define the DAG for the predict module
predict_dag = DAG(
    'predict_dag',
    schedule_interval='0 0 * * *',
    default_args=default_args,
    catchup=False
)

predict_task = PythonOperator(
    task_id='predict_task',
    python_callable=predict,
    dag=predict_dag
)

# Определение порядка выполнения
train_cancellations_task >> train_demand_task
train_demand_task >> predict_task
