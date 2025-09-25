import boto3, csv
client = boto3.client('compute-optimizer')

def iterate_recs():
    token=None
    while True:
        kwargs={}
        if token:
            kwargs['nextToken']=token
        resp = client.get_ec2_instance_recommendations(**kwargs)
        for r in resp.get('instanceRecommendations',[]):
            yield r
        token = resp.get('nextToken')
        if not token:
            break

if __name__ == "__main__":
    rows=[]
    for r in iterate_recs():
        rows.append({
            'instanceArn': r.get('instanceArn'),
            'accountId': r.get('accountId'),
            'currentType': r.get('currentInstanceType'),
            'finding': r.get('finding'),
            'recommendationOptions': str(r.get('recommendationOptions',[]))
        })
    keys = rows[0].keys() if rows else []
    with open('compute_optimizer_recs.csv','w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote compute_optimizer_recs.csv")