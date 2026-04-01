variable "snowflake_organization_name" {}
variable "snowflake_account_name" {}
variable "snowflake_user" {}
variable "snowflake_password" {
  sensitive = true
}
