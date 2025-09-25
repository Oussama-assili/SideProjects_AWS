import boto3

s3 = boto3.client('s3')

def set_lifecycle(bucket_name):
    lifecycle_config = {
        'Rules': [
            {
                'ID': 'TransitionToGlacier',
                'Status': 'Enabled',
                'Prefix': '',
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'GLACIER'}
                ],
                'Expiration': {'Days': 3650}
            }
        ]
    }
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration=lifecycle_config
    )
    print(f"Lifecycle policy applied to {bucket_name}")

if __name__ == "__main__":
    set_lifecycle("my-source-bucket-12345")
    set_lifecycle("my-backup-bucket-12345")