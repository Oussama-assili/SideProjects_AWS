terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = { source = "hashicorp/aws" }
    kubernetes = { source = "hashicorp/kubernetes" }
    helm = { source = "hashicorp/helm" }
  }
}

provider "aws" {
  region = var.region
}