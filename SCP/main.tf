# Specifies the required providers and Terraform version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = "~> 1.8.0"
}

# Configures the AWS provider with the specified region
provider "aws" {
  region = var.aws_region
}

# Defines a map of policies with their names, types, file paths, and target organizational unit IDs
locals {
  policies = {
    "policy1" = {
      policy_name      = "TAPIv2 Tag Policy 1"
      policy_type      = "TAG_POLICY"
      policy_file_path = "policies/TAPIv2_tag_policy_1.json"
      target_ou_id     = var.target_ou_id_1
    },
    "policy2" = {
      policy_name      = "TAPIv2 Tag Policy 2"
      policy_type      = "TAG_POLICY"
      policy_file_path = "policies/TAPIv2_tag_policy_2.json"
      target_ou_id     = var.target_ou_id_1
    },
    "policy3" = {
      policy_name      = "TAPIv2 AdminEmail tag SCP (1)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_AdminEmail_tag_SCP_1.json"
      target_ou_id     = var.target_ou_id_1
    },
    "policy4" = {
      policy_name      = "TAPIv2 AdminEmail tag SCP (2)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_AdminEmail_tag_SCP_2.json"
      target_ou_id     = var.target_ou_id_1
    },
    "policy5" = {
      policy_name      = "TAPIv2 AppCategory tag SCP (1)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_AppCategory_tag_SCP_1.json"
      target_ou_id     = var.target_ou_id_2
    },
    "policy6" = {
      policy_name      = "TAPIv2 AppCategory tag SCP (2)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_AppCategory_tag_SCP_2.json"
      target_ou_id     = var.target_ou_id_2
    },
    "policy7" = {
      policy_name      = "TAPIv2 Brand tag SCP (1)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_Brand_tag_SCP_1.json"
      target_ou_id     = var.target_ou_id_2
    },
    "policy8" = {
      policy_name      = "TAPIv2 Brand tag SCP (2)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_Brand_tag_SCP_2.json"
      target_ou_id     = var.target_ou_id_2
    },
    "policy9" = {
      policy_name      = "TAPIv2 DataClassification tag SCP"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_DataClassification_tag_SCP.json"
      target_ou_id     = var.target_ou_id_3
    },
    "policy10" = {
      policy_name      = "TAPIv2 DeploymentType tag SCP (1)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_DeploymentType_tag_SCP_1.json"
      target_ou_id     = var.target_ou_id_3
    },
    "policy11" = {
      policy_name      = "TAPIv2 DeploymentType tag SCP (2)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_DeploymentType_tag_SCP_2.json"
      target_ou_id     = var.target_ou_id_3
    },
    "policy12" = {
      policy_name      = "TAPIv2 EndpointType tag SCP"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_EndpointType_tag_SCP.json"
      target_ou_id     = var.target_ou_id_3
    },
    "policy13" = {
      policy_name      = "TAPIv2 Environment tag SCP (1)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_Environment_tag_SCP_1.json"
      target_ou_id     = var.target_ou_id_4
    },
    "policy14" = {
      policy_name      = "TAPIv2 Environment tag SCP (2)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_Environment_tag_SCP_2.json"
      target_ou_id     = var.target_ou_id_4
    },
    "policy15" = {
      policy_name      = "TAPIv2 Exposure tag SCP"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_Exposure_tag_SCP.json"
      target_ou_id     = var.target_ou_id_4
    },
    "policy16" = {
      policy_name      = "TAPIv2 OwningOrg tag SCP (1)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_OwningOrg_tag_SCP_1.json"
      target_ou_id     = var.target_ou_id_4
    },
    "policy17" = {
      policy_name      = "TAPIv2 OwningOrg tag SCP (2)"
      policy_type      = "SERVICE_CONTROL_POLICY"
      policy_file_path = "policies/TAPIv2_OwningOrg_tag_SCP_2.json"
      target_ou_id     = var.target_ou_id_4
    },
  }
}

# Iterates over the policies map to create multiple instances of the org_policy module
# module "TAPIv2_SCPs" {
#   for_each           = local.policies
#   source             = "./modules/org_policy"
#   policy_name        = each.value.policy_name
#   policy_description = "TAPIv2 - Prevents the creation of resources without the specified tag or set of values."
#   policy_type        = each.value.policy_type
#   policy_file_path   = each.value.policy_file_path
#   target_ou_id       = each.value.target_ou_id
# }
module "TAPIv2_SCPs" {
  source             = "./modules/org_policy"
  policy_name        = "TAPIv2 - Tag Policy Test"
  policy_description = "TAPIv2 - Prevents the creation of resources without the specified tag or set of values."
  policy_type        = "TAG_POLICY"
  policy_file_path   = "policies/TAPIv2_tag_policy_1.json"
  target_ou_id       = var.target_ou_id_1
}