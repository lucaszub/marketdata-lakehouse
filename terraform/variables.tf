variable "snowflake_organization_name" {}
variable "snowflake_account_name" {}
variable "snowflake_account" {}
variable "snowflake_user" {}
variable "snowflake_password" {
  sensitive = true
}

variable "azure_subscription_id" {}
