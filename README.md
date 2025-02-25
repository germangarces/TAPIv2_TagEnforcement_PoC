# TAPIv2_TagEnforcement_PoC
This repository hosts a PoC for TAPIv2 Tagging Enforcement. It includes IaC for AWS SCPs, AWS IAM Policies, Cloud Custodian, and Checkov, along with a set of tailored policies for each tool.

## Service Control Policies

Are being deployed to DevOps Eu Staging AWS account.

## Cloud Custodian

### Deploy Cloud Custodian

> The deployed role has the `AmazonS3ReadOnlyAccess` IAM policy attached to it.

#### 1. Build and push the docker image

```bash
docker build -t softwareplant/custodian:latest .
docker push softwareplant/custodian:latest
```

#### 2. Create an IAM OIDC provider for your cluster

```bash
cluster_name=devops-dts-ohio-aio
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
```
Determine whether an IAM OIDC provider with your cluster’s issuer ID is already in your account.

```bash
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
```

**If output is returned, then you already have an IAM OIDC provider for your cluster and you can skip the next step.** If no output is returned, then you must create an IAM OIDC provider for your cluster.

Create an IAM OIDC identity provider for your cluster with the following command.

```bash
eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve
```

#### 3. Create the IAM role and service account

(Optional) Create IAM Policy

```bash
aws iam create-policy --policy-name custodian-policy --policy-document file://infrastructure/aws-iam-policy.json
```

Create and associate IAM Role

We use `eksctl`. Install with `brew tap weaveworks/tap & brew install weaveworks/tap/eksctl`.

```bash
eksctl create iamserviceaccount --name custodian-sa --namespace devops --cluster $cluster_name \
    --role-name custodian-role \
    --attach-policy-arn arn:aws:iam::111122223333:policy/my-policy --approve
```