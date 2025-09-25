# (same content as previous adapted)
import boto3, pandas as pd
from datetime import datetime, timedelta

def iso_date(days_ago=0):
    d = datetime.utcnow().date() - timedelta(days=days_ago)
    return d.strftime('%Y-%m-%d')

def get_cost_by_service(start,end):
    client = boto3.client('ce')
    resp = client.get_cost_and_usage(
        TimePeriod={'Start':start,'End':end},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type':'DIMENSION','Key':'SERVICE'},{'Type':'DIMENSION','Key':'REGION'}]
    )
    return resp

def resp_to_df(resp):
    rows=[]
    for r in resp.get('ResultsByTime',[]):
        tstart = r['TimePeriod']['Start']
        for g in r.get('Groups',[]):
            keys = g['Keys']
            service = keys[0]
            region = keys[1] if len(keys)>1 else None
            amount = float(g['Metrics']['UnblendedCost']['Amount'])
            rows.append({'date':tstart,'service':service,'region':region,'unblended_cost':amount})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    end = iso_date(0)
    start = iso_date(30)
    print(f"Generating cost report {start}..{end}")
    resp = get_cost_by_service(start,end)
    df = resp_to_df(resp)
    df.to_excel('cost_report.xlsx', index=False)
    print("Saved cost_report.xlsx")
