# Sentinel's Journal

This journal is for CRITICAL security learnings only.

## 2024-05-23 - Exposição de Segredos e Falta de Validação na Inicialização
**Vulnerability:** Segredos como 'SENHA_BASE' estavam hardcoded no código fonte e não havia verificação se variáveis essenciais foram carregadas.
**Learning:** Hardcoding de segredos facilita vazamentos e a falta de verificações 'fail-secure' permite que a aplicação rode em estado inseguro.
**Prevention:** Sempre carregar segredos de variáveis de ambiente e implementar verificações críticas no startup que encerram a aplicação se os segredos estiverem ausentes.
