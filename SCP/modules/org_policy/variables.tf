variable "policy_name" {
  description = "Policy name"
  type        = string
  nullable    = false
}

variable "policy_description" {
  description = "Policy description"
  type        = string
}

variable "policy_type" {
  description = "Policy type"
  type        = string
  nullable    = false
  validation {
    condition     = contains(["TAG_POLICY", "SERVICE_CONTROL_POLICY"], var.policy_type)
    error_message = "The policy type must be TAG_POLICY or SERVICE_CONTROL_POLICY."
  }
}

variable "policy_file_path" {
  description = "Policy JSON file path"
  type        = string
  nullable    = false
}

variable "target_ou_id" {
  description = "Organizational Unit (OU) ID"
  type        = string
  nullable    = false
}
