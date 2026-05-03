import boto3

def check_public_buckets():
    s3 = boto3.client('s3')
    findings = []
    
    response = s3.list_buckets()
    buckets = response['Buckets']
    
    if not buckets:
        print("No S3 buckets found")
        return findings
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        print(f"Checking bucket: {bucket_name}")
        
        try:
            public_access = s3.get_public_access_block(
                Bucket=bucket_name
            )
            config = public_access[
                'PublicAccessBlockConfiguration'
            ]
            
            if not all([
                config['BlockPublicAcls'],
                config['IgnorePublicAcls'],
                config['BlockPublicPolicy'],
                config['RestrictPublicBuckets']
            ]):
                findings.append({
                    "severity": "HIGH",
                    "resource": bucket_name,
                    "issue": "S3 bucket has public access enabled",
                    "fix": "Enable Block Public Access settings"
                })
        except Exception:
            findings.append({
                "severity": "CRITICAL",
                "resource": bucket_name,
                "issue": "No public access block configured",
                "fix": "Enable Block Public Access immediately"
            })
    
    return findings