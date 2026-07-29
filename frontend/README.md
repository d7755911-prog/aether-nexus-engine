![Backblaze B2](https://img.shields.io/badge/Backblaze%20B2-Vault%20Active-green)
![Genblaze SDK](https://img.shields.io/badge/Genblaze-Primary%20Ready-blue)
![Provenance](https://img.shields.io/badge/SHA256-Provenance%20Ledger-purple)

# 🌌 Aether Spatial Studio (NEXA Engine)
> **Production-Grade Generative Spatial Compute & Provenance Engine**
> *Built for the Backblaze Generative AI Media Hackathon (2026)*

---

## 🏆 Project Overview

**Aether Spatial Studio** is a high-performance spatial compute platform designed to bridge real-time WebGL interactive 3D rendering with generative AI orchestration and durable object storage. 

Unlike standard generative AI wrappers that handle flat 2D media or stateless API calls, Aether Spatial Studio treats 3D spatial meshes as version-controlled data pipelines—enabling real-time mesh synthesis, Git-like spatial graph lineage (DAG), and cryptographic provenance vaulting on **Backblaze B2**.

---

## ✨ Key Features & Architecture

* **🎮 Real-Time Interactive WebGL Viewport:** Supports dynamic geometry switching (Sphere, Cube, Torus, Plane) with real-time PBR shader controls (Roughness, Metalness, Surface Wavefronts).
* **🧬 Spatial Asset Lineage Tree (DAG):** Full node topology version control with single-click rollback capabilities and commit hash state tracking.
* **🛡️ Backblaze B2 Spatial Vault:** Every synthesized mesh and spatial coordinate map is cryptographically hashed with `SHA-256` and logged to Backblaze B2 storage for production-grade provenance.
* **⚡ Genblaze Multi-Tier Orchestration:** Live fallback circuit breaker routing between primary and secondary generative providers (`Genblaze-Primary` <-> `Genblaze-Fallback`) with real-time latency telemetry.
* **📦 Exportable Asset Manifests:** Instant generation of standardized JSON + WebGL asset packages bound to Backblaze B2 bucket storage.

---

## 🏗️ System Architecture

                             +-----------------------+
                             |  Spatial Prompt / UI  |
                             +-----------+-----------+
                                         |
                                         v
                       +-----------------------------------+
                       |   Genblaze SDK Router Kernel      |
                       |  (Primary vs Fallback Telemetry)  |
                       +-----------------+-----------------+
                                         |
                  +----------------------+----------------------+
                  |                                             |
                  v                                             v
   +------------------------------+             +-------------------------------+
   |    WebGL Viewport Engine     |             |   Backblaze B2 Spatial Vault  |
   |  (Dynamic Geometry & PBR)    |             |  (SHA-256 Provenance & JSON)  |
   +------------------------------+             +-------------------------------+
                  |                                             |
                  +----------------------+----------------------+
                                         |
                                         v
                           +---------------------------+
                           | Spatial Lineage DAG Tree  |
                           |    (Commit & Rollback)    |
                           +---------------------------+

---

## 🚀 Getting Started

### Prerequisites

- **Node.js**: `v18.x` or higher
- **Package Manager**: `npm`, `pnpm`, or `yarn`
- **Backblaze B2 Account Credentials** (Application Key ID & Application Key)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/aether-spatial-studio.git](https://github.com/your-username/aether-spatial-studio.git)
   cd aether-spatial-studio
Install Dependencies:

Bash
npm install
Set Up Environment Variables:
Create a .env.local file in the root directory:

Code snippet
NEXT_PUBLIC_B2_KEY_ID=your_backblaze_key_id
NEXT_PUBLIC_B2_APPLICATION_KEY=your_backblaze_application_key
NEXT_PUBLIC_B2_BUCKET_NAME=your_spatial_vault_bucket
Run the Development Server:

Bash
npm run dev
Open http://localhost:3000 in your browser to view the application.

🔒 Backblaze B2 & Genblaze Integration Highlights
B2 Storage & Provenance: The application logs asset state manifests (provenance_manifest.json) containing timestamp, commit SHA, texture URLs, and telemetry metrics directly to Backblaze B2 Cloud Object Storage.

Genblaze Workflow: Utilizes the Genblaze Python/Node orchestration patterns to handle generative model fallback logic and active node synthesis.

🛠️ Tech Stack
Frontend Framework: Next.js (App Router), TypeScript, Tailwind CSS

3D Graphics Engine: Three.js / WebGL / React Three Fiber

Cloud Storage & Vaulting: Backblaze B2 Cloud Storage API

AI Orchestration: Genblaze SDK Architecture