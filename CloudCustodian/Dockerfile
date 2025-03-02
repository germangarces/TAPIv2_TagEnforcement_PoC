# Use the official Python 3.9 slim image
FROM python:3.9-slim
LABEL authors="german.garces@appfire.com"

# Install git and Cloud Custodian
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* && pip install c7n

# Copy the policies
COPY CloudCustodian/policies/ /app/policies

# Copy the information about the accounts
COPY CloudCustodian/accounts.yml /app/accounts.yml

# Set the working directory
WORKDIR /app

# Start command: adjust according to the policies file and parameters you need
# 0.1.0-alpha.1
CMD ["custodian", "run", "--output-dir", "output", "--region", "us-east-2",  "policies/policy.yml"]