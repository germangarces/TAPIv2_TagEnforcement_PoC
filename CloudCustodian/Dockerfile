# Use the official Python 3.9 slim image
FROM python:3.9-slim
LABEL authors="german.garces@appfire.com"

# Workaround for Netskope SSL interception
COPY netskope-cert-bundle.pem /cert
ENV REQUESTS_CA_BUNDLE="/cert"
ENV GIT_SSL_CAINFO="/cert"

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Cloud Custodian directly
RUN pip install c7n c7n-org

# Clone the repository into /app
# Copy the policies
COPY policies/ /policies
#RUN git clone https://github.com/germangarces/TAPIv2_TagEnforcement_PoC.git /app

# Set the working directory
WORKDIR /app

# Start command: adjust according to the policies file and parameters you need
CMD ["custodian", "run", "--dry-run",  "--output-dir", "output", "--region", "all",  "/policies/"]

