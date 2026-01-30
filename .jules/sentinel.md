# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2025-05-22 - [CRITICAL] Hardcoded Secrets Migration
**Vulnerability:** Hardcoded `SENHA_BASE` and `OWNER` email in `supremo_rpg_final.py` posed a risk of credential exposure through source code.
**Learning:** Hardcoded credentials are a common but critical vulnerability in initial project phases. Moving them to environment variables using `python-dotenv` is the standard fix.
**Prevention:** Implement a 'fail-secure' startup check that verifies the presence of mandatory secrets. If a secret like `SENHA_BASE` is missing, the application must terminate immediately to prevent unauthenticated or insecure execution. Always update `.gitignore` to include `.env` and Python build artifacts.
