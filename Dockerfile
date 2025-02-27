# Step 1: Use Python 3.12 as a base image
FROM python:3.12-slim

# Step 2: Install Poetry (Poetry is needed to install Python dependencies)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry binary path to PATH
ENV PATH="/root/.local/bin:$PATH"

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy `pyproject.toml` and `poetry.lock` first to install dependencies separately
COPY pyproject.toml poetry.lock* /app/

# Step 5: Install dependencies with Poetry
RUN poetry install --no-dev --no-interaction

# Step 6: Copy the rest of the application code
COPY . /app

# Step 7: Expose the port that Cloud Run listens to (default 8080)
EXPOSE 8080

# Step 8: Run the Flask app using Poetry
CMD ["poetry", "run", "python", "app.py"]
