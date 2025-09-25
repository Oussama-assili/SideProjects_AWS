import boto3, os

s3 = boto3.resource('s3')
SRC_BUCKET = os.environ['SRC_BUCKET']
DST_BUCKET = os.environ['DST_BUCKET']
PREFIX = os.environ.get('PREFIX', '')

def lambda_handler(event, context):
    src = s3.Bucket(SRC_BUCKET)
    dst = s3.Bucket(DST_BUCKET)
    copied = 0
    for obj in src.objects.filter(Prefix=PREFIX):
        dst.copy({'Bucket': SRC_BUCKET, 'Key': obj.key}, obj.key)
        copied += 1
    return {"copied": copied}