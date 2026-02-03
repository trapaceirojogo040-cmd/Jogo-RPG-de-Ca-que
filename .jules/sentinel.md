# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2025-05-14 - [CRITICAL] Hardcoded Secrets in Source Code
**Vulnerability:** Found hardcoded `SENHA_BASE` and `OWNER` email in `supremo_rpg_final.py`. These secrets were used for generating confirmation codes and administrative authentication.
**Learning:** Hardcoded secrets in version control are a major security risk. The application lacked a mechanism to load configuration from the environment and a "fail-secure" check to ensure it doesn't run without proper security settings.
**Prevention:** Always use environment variables for secrets. Implement a startup check (`verificar_inicializacao`) that validates the presence of required environment variables and terminates the application if they are missing. Use `python-dotenv` for local development management.
