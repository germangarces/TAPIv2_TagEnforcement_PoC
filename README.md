# TAPIv2_TagEnforcement_PoC
This repository hosts a PoC for TAPIv2 Tagging Enforcement. It includes IaC for AWS SCPs, AWS IAM Policies and Cloud Custodian, along with a set of tailored policies for each tool.

☣️ A brief summary of our tagging policy approaches with direct focus on **risks and limitations** can be found on [the Wiki](https://github.com/germangarces/TAPIv2_TagEnforcement_PoC/wiki).

### 1. Service Control Policies

**Deployment:**

This project leverages Terraform to deploy AWS Service Control Policies (SCPs).

A map holds each SCP’s details (e.g., name and path), and the `main.tf` iterates over this map to create each SCP, attaching it to an Organizational Unit provided as a parameter.

**Policy Files:**

Policies are located in the `SCP/policies` directory.

### 2. IAM Policies

**Deployment:**

There is no IaC yet. The policies are manually created in the AWS Console.

**Policy Files:**

Policies are located in the `IAM/policies` directory. Each policy is defined in a separate file.

### 3. Cloud Custodian

**Docker Image & Pipeline:**

The Cloud Custodian application and its policies are combined into a Docker image. This image can be built and pushed via a GitHub Actions pipeline (see [build-push-custodian-docker-image.yml](https://github.com/germangarces/TAPIv2_TagEnforcement_PoC/actions/workflows/build-push-custodian-docker-image.yml)).

**Policy Files:**

Policies are located in the `CloudCustodian/policies` directory.

**Deployment:**

The Docker image is deployed as a cronjob on an EKS cluster within the AWS DevOps DTS account (ID: `891377226793`).

**Authentication:**

> This was done using AWS Documentation. Here is the [link](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)

Authentication is managed through a service account and a role that includes the following policies:

- `ResourceGroupsandTagEditorFullAccess`
- `ResourceGroupsTaggingAPITagUntagSupportedResources`
- `ReadOnlyAccess`

The role is created by Justin Spies and managed via Terraform.

> Authentication to DockerHub is done via a secret in the Kubernetes cluster.

**Infrastructure Configuration:**

The service account and cronjob configuration are defined in the `CloudCustodian/infrastructure` directory.

**Policy Validation:**

Changes to the policies are automatically validated through GitHub Actions. You can also validate them locally using:

```bash
custodian validate CloudCustodian/policies/
```

## Disclaimer:

I acknowledge there are areas for improvement, but I will not proceed with any changes until we agree on the solution to implement.

**Possible Improvements:**

- Automate the deployment of IAM policies.
- Develop a tool that lets us define policies in an agnostic format, automatically translating and distributing them in each tool's required format.
- Implement a CI/CD pipeline for any of the approaches.
- Improve the credential management for Cloud Custodian deployment
- Sync with Lukasz and it's Checkov.io implementation.