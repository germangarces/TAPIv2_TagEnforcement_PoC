variable "aws_region" {
  description = "AWS Region"
  type        = string
  nullable    = false
  default     = "us-east-1"
}

variable "target_ou_id_1" {
  description = "The AWS Organization Unit ID to attach the policy to."
  type        = string
  nullable    = false
  default     = "156041420045" # DevOps EU Staging
}

variable "target_ou_id_2" {
  description = "The AWS Organization Unit ID to attach the policy to."
  type        = string
  nullable    = false
  default     = "156041420045" # DevOps EU Staging
}

variable "target_ou_id_3" {
  description = "The AWS Organization Unit ID to attach the policy to."
  type        = string
  nullable    = false
  default     = "156041420045" # DevOps EU Staging
}

variable "target_ou_id_4" {
  description = "The AWS Organization Unit ID to attach the policy to."
  type        = string
  nullable    = false
  default     = "156041420045" # DevOps EU Staging
}