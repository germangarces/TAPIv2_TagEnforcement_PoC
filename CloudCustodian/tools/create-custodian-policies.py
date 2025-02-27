#!/usr/bin/env python3
import os
import yaml


# This class is used to force literal block style (using "|" in YAML) for the comment field.
class LiteralStr(str):
    pass


def literal_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')


yaml.add_representer(LiteralStr, literal_str_representer)


def create_policy(resource):
    """
    Create a policy dictionary for a given resource.
    The resource string "aws.ec2" becomes "ec2" for the policy.
    """
    # Remove the "aws." prefix for the policy definition.
    resource_name = resource.replace("aws.", "")

    return {
        "name": f"{resource_name}-tag-compliance",
        "resource": resource_name,
        "comment": LiteralStr("Report on total count of non compliant instances"),
        "filters": [
            {"or": [
                {"tag:Environment": "absent"}
            ]}
        ]
    }


def main():
    # List of resources.
    resources = [
        "aws.ec2",
        "aws.batch-compute",
        "aws.batch-definition",
        "aws.datasync-task",
        "aws.elasticbeanstalk",
        "aws.lambda",
        "aws.lightsail-instance",
        "aws.ec2-spot-fleet-request",
        "aws.asg",
        "aws.ecs",
        "aws.ecs-container-instance",
        "aws.ecs-task-definition",
        "aws.eks",
        "aws.backup-vault",
        "aws.fsx",
        "aws.s3",
        "aws.route-table",
        "aws.security-group",
        "aws.apigwv2",
        "aws.distribution",
        "aws.customer-gateway",
        "aws.elastic-ip",
        "aws.elb",
        "aws.internet-gateway",
        "aws.nat-gateway",
        "aws.network-acl",
        "aws.eni",
        "aws.prefix-list",
        "aws.r53domain",
        "aws.shield-protection",
        "aws.vpc",
        "aws.vpc-endpoint",
        "aws.flow-log",
        "aws.peering-connection",
        "aws.vpn-gateway",
        "aws.waf",
        "aws.wafv2",
        "aws.waf-regional",
        "aws.dynamodb-table",
        "aws.cache-cluster",
        "aws.rds",
        "aws.rds-cluster",
        "aws.redshift",
        "aws.rds-cluster-snapshot",
        "aws.rds-snapshot",
        "aws.account",
        "aws.acm-certificate",
        "aws.cloudtrail",
        "aws.identity-pool",
        "aws.user-pool",
        "aws.iam-policy",
        "aws.iam-role",
        "aws.org-policy",
        "aws.iam-certificate",
        "aws.iam-user",
        "aws.iam-oidc-provider",
        "aws.iam-saml-provider",
        "aws.secrets-manager",
        "aws.ses-email-identity",
        "aws.key-pair",
        "aws.cfn",
        "aws.alarm",
        "aws.composite-alarm",
        "aws.log-group",
        "aws.event-bus",
        "aws.org-unit",
        "aws.rds-subscription",
        "aws.catalog-portfolio",
        "aws.catalog-product",
        "aws.ssm-document",
        "aws.ssm-parameter",
        "aws.step-machine",
        "aws.workspaces",
        "aws.sagemaker-model",
        "aws.athena-work-group",
        "aws.glue-crawler",
        "aws.glue-job",
        "aws.kinesis",
        "aws.kinesis-video",
        "aws.firehose",
        "aws.sns",
        "aws.sqs"
    ]

    # Name of the YAML file where policies are stored.
    output_file = "policies.yml"

    # If the file exists, load its content; otherwise, start with an empty dictionary.
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    # Ensure there is a 'policies' list in the data.
    if "policies" not in data or data["policies"] is None:
        data["policies"] = []

    # Create and append a policy for each resource.
    for resource in resources:
        policy = create_policy(resource)
        data["policies"].append(policy)

    # Write the updated data back to the file.
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


if __name__ == "__main__":
    main()
