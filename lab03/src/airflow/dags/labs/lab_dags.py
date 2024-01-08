import datetime as dt
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from labs.data_process import read_data, preprocess_data, prepare_model, check_model

# Declare Default arguments for the DAG
default_args = {
    'start_date': pendulum.datetime(2023, 11, 27, tz="UTC"),
    'catchup': False,
    'is_paused_upon_creation': True,
    'provide_context': True,
}

# Creating a new DAG
dag = DAG(
    "dataflow_process_dag",
    default_args=default_args,
    schedule_interval="0 3 * * *",
    max_active_runs=1,
)

# Define PythonOperators
read_data_op = PythonOperator(task_id="read_data", python_callable=read_data, dag=dag)
preprocess_data_op = PythonOperator(task_id="preprocess_data", python_callable=preprocess_data, dag=dag)
prepare_model_op = PythonOperator(task_id="prepare_model", python_callable=prepare_model, dag=dag)
check_model_op = PythonOperator(task_id="check_model", python_callable=check_model, dag=dag)

# Set the task sequence
read_data_op >> preprocess_data_op >> prepare_model_op >> check_model_op
