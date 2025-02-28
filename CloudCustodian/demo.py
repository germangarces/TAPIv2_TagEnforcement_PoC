#!/usr/bin/env python3
import sys
import time

from kubernetes import client, config, utils


class KubernetesDeployer:
    """
    This class encapsulates operations for deploying and cleaning up Kubernetes resources
    using the official Kubernetes Python client.
    """

    def __init__(self, namespace="devops", verbose=True):
        self.namespace = namespace
        self.verbose = verbose
        # Load Kubernetes configuration from the default location (~/.kube/config)
        config.load_kube_config()
        self.api_client = client.ApiClient()
        self.batch_api = client.BatchV1Api(self.api_client)  # For Job operations
        self.core_api = client.CoreV1Api(self.api_client)  # For ServiceAccount and Pod logs
        self.cronjob_api = client.BatchV1Api(self.api_client)  # For Cronjobs

    def log(self, message):
        if self.verbose:
            print(message)

    def deploy_yaml(self, file_path):
        """
        Deploys Kubernetes resources from a YAML file.
        """
        self.log(f"Deploying YAML from file: {file_path}")
        try:
            utils.create_from_yaml(self.api_client, file_path, namespace=self.namespace)
            self.log(f"Successfully deployed YAML: {file_path}")
        except Exception as e:
            print(f"Error deploying {file_path}: {str(e)}")
            sys.exit(1)

    def create_job_from_cronjob(self, cronjob_name, job_name):
        """
        Creates a Job based on the job template of an existing CronJob.
        """
        self.log(f"\nCreating job '{job_name}' from CronJob '{cronjob_name}'")
        try:
            # Read the CronJob object from the specified namespace using the CronJob API
            cronjob = self.cronjob_api.read_namespaced_cron_job(name=cronjob_name, namespace=self.namespace)
            # Extract the job template from the CronJob spec
            job_template = cronjob.spec.job_template
            # Build a new Job object using the job template spec and a new name
            job_metadata = client.V1ObjectMeta(name=job_name)
            job = client.V1Job(
                api_version="batch/v1",
                kind="Job",
                metadata=job_metadata,
                spec=job_template.spec
            )
            self.batch_api.create_namespaced_job(namespace=self.namespace, body=job)
            self.log(f"Job '{job_name}' created successfully.")
        except Exception as e:
            print(f"Error creating job from CronJob {cronjob_name}: {str(e)}")
            sys.exit(1)

    def wait_for_job_completion(self, job_name, timeout=300):
        """
        Polls the Job status until it completes successfully or the timeout is reached.
        """
        self.log(f"\nWaiting for job '{job_name}' to complete (timeout: {timeout} seconds)...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                job = self.batch_api.read_namespaced_job(name=job_name, namespace=self.namespace)
                if job.status.succeeded and job.status.succeeded >= 1:
                    self.log(f"Job '{job_name}' has completed successfully.")
                    return
            except Exception as e:
                print(f"Error checking job status for {job_name}: {str(e)}")
            time.sleep(5)
        print(f"Timeout reached while waiting for job '{job_name}' to complete.")
        sys.exit(1)

    def get_job_pod_logs(self, job_name):
        """
        Retrieves the logs from the pod associated with the specified Job.
        """
        self.log(f"\nFetching logs for job '{job_name}'")
        try:
            # List pods with the label "job-name=<job_name>"
            pod_list = self.core_api.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"job-name={job_name}"
            )
            if not pod_list.items:
                self.log(f"No pods found for job '{job_name}'.")
                return ""
            pod_name = pod_list.items[0].metadata.name
            logs = self.core_api.read_namespaced_pod_log(name=pod_name, namespace=self.namespace)
            return logs
        except Exception as e:
            print(f"Error retrieving logs for job {job_name}: {str(e)}")
            return ""

    def delete_cronjob(self, cronjob_name):
        """
        Deletes a CronJob resource by name.
        """
        self.log(f"Deleting CronJob '{cronjob_name}'")
        try:
            self.cronjob_api.delete_namespaced_cron_job(name=cronjob_name, namespace=self.namespace)
            self.log(f"CronJob '{cronjob_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting CronJob '{cronjob_name}': {str(e)}")

    def delete_service_account(self, sa_name):
        """
        Deletes a ServiceAccount resource by name.
        """
        self.log(f"Deleting ServiceAccount '{sa_name}'")
        try:
            self.core_api.delete_namespaced_service_account(name=sa_name, namespace=self.namespace)
            self.log(f"ServiceAccount '{sa_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting ServiceAccount '{sa_name}': {str(e)}")


def main():
    # Warn the user about AWS role prerequisites before proceeding.
    print("WARNING: Ensure that the AWS accounts to be analyzed have the necessary role with required permissions,")
    print("and that the role is assumable by the appropriate entity.")
    confirm = input("Do you want to proceed with the deployment? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deployment cancelled by the user.")
        sys.exit(0)

    # Initialize the KubernetesDeployer
    deployer = KubernetesDeployer(namespace="devops", verbose=True)

    # Deploy the ServiceAccount YAML
    deployer.deploy_yaml("CloudCustodian/infrastructure/custodian-sa.yaml")

    # Deploy the CronJobs YAMLs
    deployer.deploy_yaml("CloudCustodian/infrastructure/custodian-cronjob.yaml")
    deployer.deploy_yaml("CloudCustodian/infrastructure/custodian-multi-account-cronjob.yaml")

    # Define CronJob names and corresponding Job names.
    # It is assumed that the CronJob names are 'custodian-cronjob' and 'custodian-multi-account-cronjob'
    cronjobs = [
        ("custodian-cronjob", "custodian-cronjob-job"),
        ("custodian-multi-account-cronjob", "custodian-multi-account-cronjob-job")
    ]

    # Create a Job from each CronJob
    for cronjob_name, job_name in cronjobs:
        deployer.create_job_from_cronjob(cronjob_name, job_name)

    # Wait for each Job to complete and then fetch and print its logs
    for _, job_name in cronjobs:
        deployer.wait_for_job_completion(job_name)
        logs = deployer.get_job_pod_logs(job_name)
        print(f"\n{'=' * 60}")
        print(f"Logs from job '{job_name}':")
        print(f"{'-' * 60}\n{logs}\n{'-' * 60}")
        print(f"{'=' * 60}\n")

    # Ask user confirmation before deleting the CronJobs and ServiceAccount
    confirm_delete = input("Do you want to delete the CronJobs and the ServiceAccount? (yes/no): ").strip().lower()
    if confirm_delete == "yes":
        # Delete each CronJob
        for cronjob_name, _ in cronjobs:
            deployer.delete_cronjob(cronjob_name)
        # Delete the ServiceAccount; assumed name is 'custodian-sa'
        deployer.delete_service_account("custodian-sa")
    else:
        print("Skipping deletion of CronJobs and ServiceAccount.")


if __name__ == "__main__":
    main()
