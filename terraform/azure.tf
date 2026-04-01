resource "azurerm_resource_group" "marketdata" {
  name     = "rg-marketdata"
  location = "westeurope"
}

resource "azurerm_container_registry" "acr" {
  name                = "marketdataregistry"
  resource_group_name = azurerm_resource_group.marketdata.name
  location            = azurerm_resource_group.marketdata.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_log_analytics_workspace" "marketdata" {
  name                = "log-marketdata"
  resource_group_name = azurerm_resource_group.marketdata.name
  location            = azurerm_resource_group.marketdata.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "marketdata" {
  name                       = "cae-marketdata"
  resource_group_name        = azurerm_resource_group.marketdata.name
  location                   = azurerm_resource_group.marketdata.location
  log_analytics_workspace_id = azurerm_log_analytics_workspace.marketdata.id
}

resource "azurerm_container_app" "streamlit" {
  name                         = "ca-marketdata-streamlit"
  resource_group_name          = azurerm_resource_group.marketdata.name
  container_app_environment_id = azurerm_container_app_environment.marketdata.id
  revision_mode                = "Single"

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  template {
    container {
      name   = "streamlit"
      image  = "${azurerm_container_registry.acr.login_server}/marketdata-streamlit:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "SNOWFLAKE_ACCOUNT"
        value = var.snowflake_account
      }
      env {
        name  = "SNOWFLAKE_USER"
        value = var.snowflake_user
      }
      env {
        name        = "SNOWFLAKE_PASSWORD"
        secret_name = "snowflake-password"
      }
      env {
        name  = "SNOWFLAKE_ROLE"
        value = "ACCOUNTADMIN"
      }
      env {
        name  = "SNOWFLAKE_WAREHOUSE"
        value = "MARKETDATA_WH"
      }
      env {
        name  = "SNOWFLAKE_DATABASE"
        value = "MARKETDATA"
      }
      env {
        name  = "SNOWFLAKE_SCHEMA"
        value = "RAW"
      }
    }

    min_replicas = 0
    max_replicas = 1
  }

  secret {
    name  = "snowflake-password"
    value = var.snowflake_password
  }

  ingress {
    external_enabled = true
    target_port      = 8501
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

output "streamlit_url" {
  value = "https://${azurerm_container_app.streamlit.ingress[0].fqdn}"
}
