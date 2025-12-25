# Sentinel's Journal

This journal contains critical security learnings specific to this codebase. Its purpose is to record high-impact vulnerabilities, unexpected fix behaviors, and reusable security patterns discovered during security audits.

## 2024-07-25 - Hardcoded Secret (`SENHA_BASE`)

**Vulnerability:** A hardcoded secret, `SENHA_BASE`, was identified in `supremo_rpg_final.py`. This secret was used as a salt for generating security confirmation codes.

**Learning:** Storing secrets directly in source code is a critical vulnerability. It makes the secret accessible to anyone with read access to the codebase, rendering security mechanisms that rely on it ineffective. The application's security confirmation protocol was fundamentally compromised by this practice.

**Prevention:** All secrets, keys, and sensitive configuration values must be loaded from environment variables. The `.gitignore` file should be configured to ignore `.env` files, and a `.env.example` file should be maintained to instruct developers on the required variables. The application must fail fast if a required secret is not provided in the environment.
