import boto3

def check_open_security_groups():
    ec2 = boto3.client('ec2', region_name='ap-southeast-1')
    findings = []
    
    sgs = ec2.describe_security_groups()['SecurityGroups']
    
    dangerous_ports = {
        22: "SSH",
        3389: "RDP",
        3306: "MySQL",
        5432: "PostgreSQL"
    }
    
    for sg in sgs:
        sg_id = sg['GroupId']
        sg_name = sg['GroupName']
        print(f"Checking security group: {sg_name}")
        
        for rule in sg['IpPermissions']:
            from_port = rule.get('FromPort', 0)
            
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    if from_port in dangerous_ports:
                        findings.append({
                            "severity": "CRITICAL",
                            "resource": f"{sg_id} ({sg_name})",
                            "issue": f"Port {from_port} ({dangerous_ports[from_port]}) open to entire internet",
                            "fix": "Restrict source IP or remove rule"
                        })
    
    return findings