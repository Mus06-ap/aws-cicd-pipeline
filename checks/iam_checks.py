import boto3

def check_users_without_mfa():
    iam = boto3.client('iam')
    findings = []
    
    users = iam.list_users()['Users']
    
    if not users:
        print("No IAM users found")
        return findings
    
    for user in users:
        username = user['UserName']
        print(f"Checking user: {username}")
        
        mfa_devices = iam.list_mfa_devices(
            UserName=username
        )['MFADevices']
        
        if len(mfa_devices) == 0:
            findings.append({
                "severity": "HIGH",
                "resource": username,
                "issue": f"IAM user {username} has no MFA enabled",
                "fix": "Enable MFA device for this user"
            })
    
    return findings

def check_root_account_usage():
    iam = boto3.client('iam')
    findings = []
    
    summary = iam.get_account_summary()['SummaryMap']
    
    if summary.get('AccountAccessKeysPresent', 0) > 0:
        findings.append({
            "severity": "CRITICAL",
            "resource": "root account",
            "issue": "Root account has active access keys",
            "fix": "Delete root account access keys immediately"
        })
    
    return findings