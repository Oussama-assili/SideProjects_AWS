# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = ">= 4.0"
  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr
  azs  = slice(data.aws_availability_zones.available.names, 0, 3)
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets
  enable_nat_gateway = true
}

data "aws_availability_zones" "available" {
  state = "available"
}

# EKS
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = ">= 17.0.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"
  subnets         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id
  enable_irsa     = true
  manage_aws_auth = true

  node_groups = {
    on_demand = {
      desired_capacity = 2
      min_capacity     = 1
      max_capacity     = 3
      instance_types   = var.node_instance_types
      key_name         = var.ssh_key_name
      tags = { Role = "on-demand" }
    }
    spot = {
      desired_capacity = 1
      min_capacity     = 0
      max_capacity     = 4
      instance_types   = ["t3a.small","t3a.medium"]
      capacity_type    = "SPOT"
      tags = { Role = "spot" }
    }
  }

  tags = {
    Environment = "prod"
    Owner = var.owner
  }

  cluster_log_types = ["api","audit","authenticator"]
}
