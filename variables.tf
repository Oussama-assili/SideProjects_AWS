variable "region" { type = string default = "eu-west-1" }
variable "cluster_name" { type = string default = "client-eks" }
variable "vpc_cidr" { type = string default = "10.100.0.0/16" }
variable "public_subnets" { type = list(string) default = ["10.100.1.0/24","10.100.2.0/24","10.100.3.0/24"] }
variable "private_subnets" { type = list(string) default = ["10.100.11.0/24","10.100.12.0/24","10.100.13.0/24"] }
variable "ssh_key_name" { type = string default = "" } # optional
variable "node_instance_types" { type = list(string) default = ["t3.medium"] }
variable "owner" { type = string default = "you@domain" }