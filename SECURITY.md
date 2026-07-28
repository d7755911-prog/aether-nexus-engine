# 🛡️ Security & Integrity Policy

## 🔒 Provenance & Encryption Standards

- **SHA-256 Provenance Seals:** Every spatial mesh synthesized by the engine generates an immutable cryptographic signature.
- **Vault Token Safety:** Backblaze B2 storage keys are stored via encrypted environment variables (`B2_APPLICATION_KEY`) and are never exposed to client-side bundles.

## ⚠️ Reporting Vulnerabilities

If you discover any security issues or token leak risks, please contact the lead architect directly via GitHub Issues using the `[SECURITY]` tag.