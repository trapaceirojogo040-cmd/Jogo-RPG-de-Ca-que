# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2025-01-24 - [Hardcoded Secrets & Fail-Secure Startup]
**Vulnerability:** Hardcoded credentials (SENHA_BASE and OWNER email) in the source code.
**Learning:** Hardcoded secrets are easily exposed in version control. A "fail-secure" startup check ensures the application cannot run without necessary environmental configuration, preventing accidental operation with default or missing security parameters.
**Prevention:** Always use environment variables for sensitive data and implement a mandatory check at application entry to validate their presence.
