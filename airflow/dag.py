from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.redis.hooks.redis import RedisHook
from datetime import datetime, timedelta
from .utils import get_current_price

currency_list = ["BTC", "ETH", "USDT", "XRP", "BNB"]

# Define default_args for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Callback function for task failures
def task_failure_callback(context):
    task_instance = context.get('task_instance')
    dag_id = task_instance.dag_id
    task_id = task_instance.task_id
    execution_date = task_instance.execution_date

    # Log failure information
    failure_message = f"Task {task_id} of DAG {dag_id} failed at {execution_date}."
    print(failure_message)

# Initialize the DAG
dag = DAG(
    'cryptocurrency_price_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),  # Run every 1 hours
    catchup=False,
    on_failure_callback=task_failure_callback  # Apply failure callback to all tasks
)

# Function to fetch cryptocurrency price data from CoinGecko
def fetch_price_data():
    for currency in currency_list:
        try:
            get_current_price(currency)
        except Exception as e:
            print(f"Error fetching price data: {e}")

# Define the Airflow task to fetch data
fetch_data_task = PythonOperator(
    task_id='fetch_price_data',
    python_callable=fetch_price_data,
    dag=dag,
)

# Dummy task to simulate completion
def success_task():
    print("Data successfully fetched and stored in Redis.")

success_task = PythonOperator(
    task_id='success_task',
    python_callable=success_task,
    dag=dag,
)


# Set up task dependencies
fetch_data_task >> success_task
