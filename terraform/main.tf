terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.98"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

provider "snowflake" {
  organization_name = var.snowflake_organization_name
  account_name      = var.snowflake_account_name
  user              = var.snowflake_user
  password          = var.snowflake_password
  role              = "ACCOUNTADMIN"
}

# Warehouse — auto-suspend après 60s pour économiser les crédits
resource "snowflake_warehouse" "marketdata_wh" {
  name           = "MARKETDATA_WH"
  warehouse_size = "X-SMALL"
  auto_suspend   = 60
  auto_resume    = true
}

# Database
resource "snowflake_database" "marketdata" {
  name = "MARKETDATA"
}

# Schema RAW — données brutes issues de l'ingestion
resource "snowflake_schema" "raw" {
  database = snowflake_database.marketdata.name
  name     = "RAW"
}

# Schema ANALYTICS — données transformées par dbt
resource "snowflake_schema" "analytics" {
  database = snowflake_database.marketdata.name
  name     = "ANALYTICS"
}

# Table de destination pour extract.py
resource "snowflake_table" "ohlcv" {
  database = snowflake_database.marketdata.name
  schema   = snowflake_schema.raw.name
  name     = "OHLCV"

  column {
    name = "TIMESTAMP"
    type = "TIMESTAMP_NTZ"
  }
  column {
    name = "TICKER"
    type = "VARCHAR(20)"
  }
  column {
    name = "OPEN"
    type = "FLOAT"
  }
  column {
    name = "HIGH"
    type = "FLOAT"
  }
  column {
    name = "LOW"
    type = "FLOAT"
  }
  column {
    name = "CLOSE"
    type = "FLOAT"
  }
  column {
    name = "VOLUME"
    type = "NUMBER(20,0)"
  }
  column {
    name = "CURRENCY"
    type = "VARCHAR(5)"
  }
  column {
    name = "INGESTED_AT"
    type = "TIMESTAMP_NTZ"
  }
}
