import boto3
from datetime import datetime, timedelta

ce = boto3.client('ce')
ec2 = boto3.client('ec2')
elbv2 = boto3.client('elbv2')
cloudwatch = boto3.client('cloudwatch')

def monthly_ce_for_usage_types(start, end, usage_types):
    resp = ce.get_cost_and_usage(
        TimePeriod={'Start':start,'End':end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        Filter={'Dimensions':{'Key':'USAGE_TYPE','Values':usage_types}},
        GroupBy=[{'Type':'DIMENSION','Key':'SERVICE'}]
    )
    results=[]
    for r in resp.get('ResultsByTime',[]):
        for g in r.get('Groups',[]):
            results.append((g['Keys'][0], float(g['Metrics']['UnblendedCost']['Amount'])))
    return results

def check_nat(start,end,threshold=20.0):
    usage_types=['NATGateway-Hours','NATGateway-Bytes']
    return [r for r in monthly_ce_for_usage_types(start,end,usage_types) if r[1]>=threshold]

def check_data_transfer(start,end,threshold=50.0):
    usage_types=['DataTransfer-Out-Bytes','DataTransfer-Regional-Bytes','DataTransfer-Internet-Bytes']
    return [r for r in monthly_ce_for_usage_types(start,end,usage_types) if r[1]>=threshold]

def list_idle_ebs():
    vols = ec2.describe_volumes(Filters=[{'Name':'status','Values':['available']}])['Volumes']
    return [{'VolumeId':v['VolumeId'],'Size':v['Size']} for v in vols]

if __name__ == "__main__":
    end = datetime.utcnow().date().replace(day=1).strftime('%Y-%m-%d')
    start = (datetime.utcnow().date().replace(day=1) - timedelta(days=30)).strftime('%Y-%m-%d')
    print("NAT findings:", check_nat(start,end))
    print("Data transfer findings:", check_data_transfer(start,end))
    print("Idle EBS:", list_idle_ebs())