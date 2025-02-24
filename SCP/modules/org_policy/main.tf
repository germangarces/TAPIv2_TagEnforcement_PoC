resource "aws_organizations_policy" "custom_policy" {
  name        = var.policy_name
  description = var.policy_description
  content     = file(var.policy_file_path)
  type        = var.policy_type
}

resource "aws_organizations_policy_attachment" "policy_attachment" {
  policy_id = aws_organizations_policy.custom_policy.id
  target_id = var.target_ou_id
}
