from checks.s3_checks import check_public_buckets
from checks.iam_checks import check_users_without_mfa, check_root_account_usage
from checks.ec2_checks import check_open_security_groups
from datetime import datetime
import os

def generate_html_report(findings, scan_time):
    critical = [f for f in findings if f['severity'] == 'CRITICAL']
    high = [f for f in findings if f['severity'] == 'HIGH']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AWS Security Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #0f1117;
            color: #e0e0e0;
        }}
        h1 {{
            color: #00d4ff;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }}
        .summary {{
            background: #1a1f2e;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            display: flex;
            gap: 30px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 48px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 14px;
            color: #888;
        }}
        .critical {{ color: #ff4444; }}
        .high {{ color: #ff8800; }}
        .green {{ color: #00cc44; }}
        .finding {{
            background: #1a1f2e;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 5px solid #ccc;
        }}
        .finding.CRITICAL {{ border-left-color: #ff4444; }}
        .finding.HIGH {{ border-left-color: #ff8800; }}
        .badge {{
            padding: 4px 12px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }}
        .badge.CRITICAL {{ background: #ff4444; }}
        .badge.HIGH {{ background: #ff8800; }}
        .meta {{
            color: #888;
            font-size: 13px;
            margin-top: 5px;
        }}
        .fix {{
            background: #0d1f0d;
            border: 1px solid #00cc44;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            color: #00cc44;
            font-size: 13px;
        }}
        .clean {{
            background: #0d1f0d;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #00cc44;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>AWS Security Posture Report</h1>
    <p class="meta">Generated: {scan_time}</p>

    <div class="summary">
        <div class="stat">
            <div class="stat-number"
            style="color:#e0e0e0">{len(findings)}</div>
            <div class="stat-label">Total Findings</div>
        </div>
        <div class="stat">
            <div class="stat-number critical">
            {len(critical)}</div>
            <div class="stat-label">Critical</div>
        </div>
        <div class="stat">
            <div class="stat-number high">
            {len(high)}</div>
            <div class="stat-label">High</div>
        </div>
    </div>
"""

    if not findings:
        html += """
    <div class="clean">
        <h2 class="green">No findings detected</h2>
        <p>Your AWS environment passed all
        security checks.</p>
    </div>
"""
    else:
        html += "<h2>Findings</h2>"
        for f in findings:
            html += f"""
    <div class="finding {f['severity']}">
        <span class="badge {f['severity']}">
        {f['severity']}</span>
        <h3 style="margin:10px 0 5px">
        {f['resource']}</h3>
        <p class="meta">{f['issue']}</p>
        <div class="fix">
        Fix: {f['fix']}</div>
    </div>
"""

    html += """
</body>
</html>"""

    os.makedirs('reports', exist_ok=True)
    filename = "reports/security_report.html"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html)
    print(f"\nReport saved: {filename}")
    return filename

def run_scanner():
    print("=" * 50)
    print("AWS SECURITY POSTURE SCANNER")
    scan_time = datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')
    print(f"Scan started: {scan_time}")
    print("=" * 50)

    all_findings = []

    print("\n[*] Checking S3 buckets...")
    all_findings += check_public_buckets()

    print("[*] Checking IAM users...")
    all_findings += check_users_without_mfa()
    all_findings += check_root_account_usage()

    print("[*] Checking Security Groups...")
    all_findings += check_open_security_groups()

    print(f"\n{'=' * 50}")
    print(f"SCAN COMPLETE - {len(all_findings)} findings")
    print(f"{'=' * 50}\n")

    critical = [f for f in all_findings
                if f['severity'] == 'CRITICAL']
    high = [f for f in all_findings
            if f['severity'] == 'HIGH']

    print(f"CRITICAL: {len(critical)}")
    print(f"HIGH:     {len(high)}")

    if all_findings:
        print("\n--- FINDINGS ---\n")
        for finding in all_findings:
            print(
                f"[{finding['severity']}] "
                f"{finding['resource']}"
            )
            print(f"  Issue: {finding['issue']}")
            print(f"  Fix:   {finding['fix']}\n")

    generate_html_report(all_findings, scan_time)
    return all_findings

if __name__ == "__main__":
    run_scanner() 