# Use the official Airflow image
FROM apache/airflow:2.5.1

# Set environment variables to avoid warnings
ENV AIRFLOW_HOME=/opt/airflow

# Install any required dependencies
RUN pip install --no-cache-dir redis requests

# Copy the DAG file into the container
COPY dags/ /opt/airflow/dags/

# Set Airflow user and execute the entrypoint script
USER airflow
ENTRYPOINT ["/entrypoint"]
CMD ["webserver"]
