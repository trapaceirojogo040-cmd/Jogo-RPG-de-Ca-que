# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2025-05-15 - Fail-Secure Startup Validation
**Vulnerability:** Hardcoded secrets and lack of environment variable validation at startup.
**Learning:** Hardcoding secrets (SENHA_BASE) in source code exposes them to anyone with read access. Failing to validate their presence in the environment at startup can lead to runtime errors or insecure default states.
**Prevention:** Use `python-dotenv` to load secrets from the environment. Implement a `verificar_inicializacao()` function that validates required variables and exits the application if they are missing.
