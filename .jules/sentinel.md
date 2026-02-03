# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2025-05-22 - Fail-Secure Startup and Secret Management
**Vulnerability:** Hardcoded secrets in source code and lack of initialization checks.
**Learning:** Hardcoded secrets are easily exposed. Running without proper configuration leads to insecure states.
**Prevention:** Use `python-dotenv` to load secrets from environment variables and implement a `verificar_inicializacao` check that terminates the app if secrets are missing.
