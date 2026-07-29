# 🤝 Contributing to AETHER-MIND Spatial Engine

Thank you for your interest in advancing the **AETHER-MIND Spatial Engine**! We welcome contributions from spatial computing engineers, WebGL developers, and AI pipeline architects.

---

## 🚀 Development Workflow

1. **Fork & Branch:** Create an isolated feature branch:
   ```bash
   git checkout -b feature/spatial-mesh-optimization
Commit Conventions: Follow strictly formatted commit tags for lineage tracking:

feat: New spatial engine capabilities, shader nodes, or UI modules

fix: Visual rendering bugs, state sync glitches, or memory leaks

perf: Mesh generation, WebGL pipeline, or latency optimizations

b2-vault: Backblaze storage schema or provenance ledger updates

Local Testing & Diagnostics:

Frontend: Verify TypeScript strict mode & production build:

Bash
npm run build
Backend & Pipelines: Ensure Python tests and SDK integration pass:

Bash
pytest tests/
Provenance Validation: Test export manifest JSON generation locally before pushing.

Submit Pull Request: Target the main branch with a clear description, linking relevant issues or DAG node references.

⚙️ Engineering Standards & Guidelines
🐍 Python Backend & Genblaze Integration
Code Style: PEP 8 compliance enforced via flake8 / black.

Type Safety: Strict typing via pydantic schemas for all B2 provenance payloads and node metadata.

Error Handling: All external model calls must implement primary/fallback circuit-breaking telemetry.

🎨 Frontend & WebGL (Three.js / React Three Fiber)
Framework: Next.js with strict TypeScript. Functional components only.

Shader / Geometry Performance: Avoid inline memory allocations inside useFrame loops to prevent dropped frames in the 3D Viewport.

State Management: Keep DAG node updates idempotent for reliable rollback support.

🔒 Security & B2 Credentials
Never commit live keys: Keep Backblaze B2 credentials, application keys, and bucket IDs strictly inside .env.local.

Use .env.example to declare required environment variables.