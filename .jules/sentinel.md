# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2025-05-14 - Implementing Fail-Secure Environment Configuration
**Vulnerability:** Hardcoded secrets in the source code (base password and owner email) were used for cryptographic signing and identity verification.
**Learning:** Hardcoded secrets are easily compromised via version control. Even in conceptual demos, they establish poor security patterns.
**Prevention:** Implement a "Fail-Secure" check at the application's entry point to validate that required environment variables are present before execution. Use `python-dotenv` for local environment management and `os.getenv` for retrieval, ensuring that the application never runs in an insecure default state.
