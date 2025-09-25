#!/usr/bin/env bash
# Usage: ./k8s-bootstrap.sh <kubeconfig-file>
KUBECONFIG_FILE=${1:-~/.kube/config}
export KUBECONFIG=$KUBECONFIG_FILE

# cert-manager
kubectl create namespace cert-manager || true
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.14.0 --set installCRDs=true

# AWS Load Balancer Controller - make sure IRSA role exists and annotation is in values
helm repo add eks https://aws.github.io/eks-charts
helm repo update
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master" || true
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system \
  --set clusterName=${CLUSTER_NAME:-client-eks} --set region=${AWS_REGION:-eu-west-1} \
  --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller

# ArgoCD (install via Helm)
kubectl create namespace argocd || true
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install argocd argo/argo-cd -n argocd
