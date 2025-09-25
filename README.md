# Cost Optimization scripts

Quick scripts to extract Cost Explorer info, detect common hidden fees, and fetch Compute Optimizer recommendations.

Install:
  pip install -r requirements.txt

Pre-req:
  - Enable Cost Explorer and Compute Optimizer in the AWS account
  - IAM with ce:GetCostAndUsage, compute-optimizer:GetEC2InstanceRecommendations, s3:GetObject if CUR is used

Usage:
  python cost_report.py        # writes cost_report.xlsx
  python detect_hidden_fees.py # prints heuristics for NAT, data transfer, idle resources
  python rightsizing_compute_optimizer.py  # writes compute_optimizer_recs.csv
