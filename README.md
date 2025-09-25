# S3 Backups & Lifecycle (Python Only)

This project demonstrates how to manage **S3 backups** and **lifecycle rules** using Python + boto3.

Features:
- Create source & backup buckets with encryption and versioning
- Apply lifecycle rules (transition to Glacier after X days, expire after Y days)
- Enable **Cross-Region Replication (CRR)** between two buckets
- Example Lambda for **scheduled backups**

## Setup
1. pip install -r requirements.txt
2. Configure AWS credentials (profile, env vars, or IAM role)
3. Run scripts individually:
   - `python create_backup_buckets.py`
   - `python setup_lifecycle_policy.py`
   - `python enable_replication.py`

For Lambda:
- Deploy `scheduled_backup_lambda.py` with environment variables:
  - `SRC_BUCKET`
  - `DST_BUCKET`
  - (Optional) `PREFIX`
