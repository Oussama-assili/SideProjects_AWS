# EKS Management - Terraform skeleton

Purpose: Provision a production-grade EKS cluster (VPC, Managed Node Groups) and bootstrap common add-ons.

Usage:
1. Edit `terraform.tfvars` or pass variables via CLI.
2. terraform init
3. terraform apply

After apply, run `k8s-bootstrap.sh` to install cert-manager, AWS LB Controller, and ArgoCD via Helm.

Note: Replace placeholders (ACCOUNT_ID, SSH_KEY_NAME). Use an admin/assume-role with enough privileges for EKS, IAM, VPC.
