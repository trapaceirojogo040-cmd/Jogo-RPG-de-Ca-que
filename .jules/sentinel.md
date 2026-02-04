## 2025-01-24 - Fail-Secure Startup Check and Secret Management
**Vulnerability:** Hardcoded credentials (password and email) in the source code.
**Learning:** The application lacked a mechanism to verify that required secrets were loaded from the environment before execution, leading to potential hardcoded values or runtime errors if missing.
**Prevention:** Implement a `verificar_seguranca()` function that validates the presence of critical environment variables at startup and terminates the process with a clear error message if any are missing. Use `python-dotenv` for local secret management.
