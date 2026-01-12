# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2024-05-23 - The Unseen .env: A Git Staging Vulnerability

**Vulnerability:** A hardcoded secret (`SENHA_BASE`) was correctly identified and moved to a `.env` file. However, the `.env` file itself was accidentally committed to the repository, negating the entire security benefit and keeping the secret exposed in the git history.

**Learning:** The `.gitignore` file was correctly configured to ignore `.env` files. The vulnerability was introduced because the `.env` file was created and staged (`git add .`) *before* the `.gitignore` rule was fully effective or respected by the staging command. Even with a correct `.gitignore`, a file can be explicitly or accidentally added to the git index.

**Prevention:** Always verify the output of `git status` *before* committing. Specifically, ensure that no sensitive files (like `.env`) appear in the "Changes to be committed" list. When removing a sensitive file that has been committed, `git rm --cached <file>` is required to unstage it from the repository's history, followed by a `delete_file` to remove it locally. Never assume `.gitignore` is a foolproof shield; always verify the staged files.
