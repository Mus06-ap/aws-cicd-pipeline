# Security Findings Log

## Finding 001
**Date:** 2026-05-03
**Severity:** HIGH
**Resource:** Musab-Admin (IAM User)
**Issue:** IAM user has no MFA enabled
**Status:** OPEN → REMEDIATED

**Evidence:**
- Scanner detected HIGH finding
- AWS Console confirmed MFA (0) devices assigned

**Remediation Steps:**
- Enabled MFA device via AWS Console
  using Google Authenticator
- Re-ran scanner to verify fix

**Result After Fix:**
- Scanner returned 0 findings
- Vulnerability resolved

**Lesson Learned:**
Even admin IAM users must have MFA enabled.
Without MFA a compromised password gives
an attacker full account access instantly.
This is one of the most common real-world
AWS misconfigurations found in production.