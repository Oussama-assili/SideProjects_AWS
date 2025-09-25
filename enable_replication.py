import boto3, json

s3 = boto3.client('s3')
iam = boto3.client('iam')

def create_replication_role(role_name, source_bucket, backup_bucket, account_id):
    assume_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "s3.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    role = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_policy)
    )
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionTagging"
                ],
                "Resource": f"arn:aws:s3:::{source_bucket}/*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags"
                ],
                "Resource": f"arn:aws:s3:::{backup_bucket}/*"
            }
        ]
    }
    iam.put_role_policy(
        RoleName=role_name,
        PolicyName="S3ReplicationPolicy",
        PolicyDocument=json.dumps(policy)
    )
    return role['Role']['Arn']

def enable_replication(source_bucket, backup_bucket, role_arn):
    config = {
        "Role": role_arn,
        "Rules": [{
            "Status": "Enabled",
            "Priority": 1,
            "Filter": {"Prefix": ""},
            "Destination": {"Bucket": f"arn:aws:s3:::{backup_bucket}"}
        }]
    }
    s3.put_bucket_replication(
        Bucket=source_bucket,
        ReplicationConfiguration=config
    )
    print(f"Replication from {source_bucket} → {backup_bucket} enabled")

if __name__ == "__main__":
    role_arn = create_replication_role(
        "s3-replication-role",
        "my-source-bucket-12345",
        "my-backup-bucket-12345",
        "123456789012"   # replace with your AWS account ID
    )
    enable_replication("my-source-bucket-12345", "my-backup-bucket-12345", role_arn)
