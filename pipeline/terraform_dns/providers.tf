terraform {
  backend "pg" {}
  required_providers {
    mikrotik = {
      source = "ddelnano/mikrotik"
      version = "0.14.0"
    }
  }
}

provider "mikrotik" {
  host           = "${var.mikrotik_host}"
  username       = "${var.mikrotik_username}"
  password       = "${var.mikrotik_password}"
  insecure       = true   
}