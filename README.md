# ⚡ AETHER-MIND Nexus Engine

![Build Status](https://img.shields.io/badge/Deployment-Render_Live-emerald?style=for-the-badge&logo=render)
![Frontend](https://img.shields.io/badge/Studio_UI-Vercel-black?style=for-the-badge&logo=vercel)
![Vault Storage](https://img.shields.io/badge/Storage-Backblaze_B2-blue?style=for-the-badge&logo=backblaze)
![Architecture](https://img.shields.io/badge/Phase_4-Zero--Downtime_Resilient-cyan?style=for-the-badge)

Enterprise-grade resilient spatial asset engine powered by **Backblaze B2 durable storage**, multi-provider fallbacks, and real-time WebGL 3D inspection.

## 🏗️ Core Architecture
- **Adaptive Circuit Breaker:** Zero-downtime provider fallback during rate limits or API failures.
- **Async B2 Telemetry Sink:** Non-blocking queueing of latency metrics and SHA-256 provenance directly to Backblaze B2.
- **DAG Version Tree & Hot-Rollback:** Real-time spatial asset graph tracking with zero-reload rollbacks.

## 🔗 Live Deployments
- **Studio UI (Vercel):** `https://aether-studio.vercel.app`
- **FastAPI Engine (Render):** `https://aether-nexus-engine.onrender.com`
