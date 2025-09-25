import boto3

s3 = boto3.client('s3')

def create_bucket(bucket_name, region="eu-west-1"):
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region}
    )
    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    # Enable SSE (AES256)
    s3.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
        }
    )
    print(f"Bucket {bucket_name} created with versioning + encryption")

if __name__ == "__main__":
    create_bucket("my-source-bucket-12345", "eu-west-1")
    create_bucket("my-backup-bucket-12345", "eu-west-2")
