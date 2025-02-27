# Use the official Python 3.9 slim image
FROM python:3.9-slim
LABEL authors="german.garces@appfire.com"

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Cloud Custodian directly
RUN pip install c7n c7n-org

# Copy the policies
COPY CloudCustodian/policies/ /app/policies

# Copy the information about the accounts
COPY CloudCustodian/accounts.yml /app/accounts.yml

# Set the working directory
WORKDIR /app

# Start command: adjust according to the policies file and parameters you need
CMD ["custodian", "run", "--output-dir", "output", "--region", "all",  "policies/"]