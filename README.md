⚡ AETHER-MIND Nexus EngineAn enterprise-grade, highly resilient spatial asset engine engineered with Backblaze B2 durable storage, multi-provider adaptive circuit breakers, and real-time WebGL 3D inspection workflows.🏗️ System Architecture & Key Capabilities⚡ Adaptive Circuit Breaker: Zero-downtime provider fallback during rate limits, high latencies, or upstream API failures.🛡️ Async B2 Telemetry Sink: Non-blocking queueing of operational metrics and SHA-256 provenance directly committed to Backblaze B2 Vault.🔄 Spatial Asset Lineage Tree (DAG): Real-time spatial asset version graph supporting single-click, hot-state rollbacks without full application reloads.🧊 Interactive WebGL Viewport: Dynamic material parameter tuning (Roughness, Metalness) and real-time mesh geometry synthesization (Sphere, Cube, Torus, Plane).🔗 Live DeploymentsStudio UI (Netlify): [https://aether-nexus-engine.netlify.app](https://aether-nexus-engine.netlify.app)FastAPI Engine (Render): [https://aether-nexus-engine-6.onrender.com](https://aether-nexus-engine-6.onrender.com)🛠️ Tech StackLayerTechnologyFrontend StudioNext.js 14, Three.js / WebGL, Tailwind CSSBackend EnginePython 3.12, FastAPI, Uvicorn, PydanticStorage VaultBackblaze B2 Spatial VaultDeploymentNetlify (Frontend Edge), Render (Backend Engine)🚀 Quick Local Setup1. Backend EngineBash# Clone repository
git clone https://github.com/d7755911-prog/aether-nexus-engine.git
cd aether-nexus-engine

# Install & Run Backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 10000
2. Frontend StudioBashcd frontend
npm install
npm run dev
Built with 🔥 for high-density spatial computing and enterprise fault tolerance.