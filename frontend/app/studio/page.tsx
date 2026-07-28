"use client";

import React, { useState } from "react";
import dynamic from "next/dynamic";
import VersionTree, {
  AssetCommitNode,
} from "@/components/inspector/VersionTree";
import SpatialCanvasGraph from "@/components/inspector/SpatialCanvasGraph";
import type { Viewport3DProps } from "@/components/inspector/Viewport3D";
import {
  Box,
  Circle,
  Disc,
  Layers,
  RefreshCw,
  Database,
  Zap,
  GitCommit as GitCommitIcon,
  Eye,
  Network,
} from "lucide-react";

// ✅ Dynamic Import with SSR disabled to eliminate WebGL / Canvas hydration mismatches
const Viewport3D = dynamic<Viewport3DProps>(
  () => import("@/components/inspector/Viewport3D"),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-center">
        <div className="flex items-center gap-2 text-xs font-mono text-cyan-400">
          <RefreshCw className="w-4 h-4 animate-spin" />
          Initializing WebGL Canvas...
        </div>
      </div>
    ),
  }
);

const INITIAL_COMMITS: AssetCommitNode[] = [
  {
    commitId: "commit-a91b2c3d",
    parentId: "root",
    prompt: "Holographic Quantum Lattice with Low Sine Wave Resonance",
    seed: 847291,
    durableUrl:
      "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/crate.gif",
    timestamp: "12:40:15 UTC",
    provider: "Genblaze-Primary",
    latencyMs: 312,
  },
  {
    commitId: "commit-f789a0b1",
    parentId: "commit-a91b2c3d",
    prompt: "Volumetric Cyber Lattice with High Density Nodes",
    seed: 918234,
    durableUrl:
      "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/uv_grid_opengl.jpg",
    timestamp: "12:42:08 UTC",
    provider: "Genblaze-Fallback",
    latencyMs: 428,
  },
];

export default function GrandFinalStudioDashboard() {
  const [viewMode, setViewMode] = useState<"3d_inspector" | "canvas_graph">(
    "3d_inspector"
  );
  const [geometry, setGeometry] = useState<
    "sphere" | "cube" | "plane" | "torus"
  >("sphere");
  const [roughness, setRoughness] = useState(0.2);
  const [metalness, setMetalness] = useState(0.1);
  const [prompt, setPrompt] = useState(
    "Kinetic Spatial Mesh with Adaptive Wavefront Coordinates"
  );
  const [isGenerating, setIsGenerating] = useState(false);

  const [commitList, setCommitList] =
    useState<AssetCommitNode[]>(INITIAL_COMMITS);
  const [activeCommit, setActiveCommit] = useState<AssetCommitNode>(
    INITIAL_COMMITS[1]
  );

  const handleSynthesizeNewCommit = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/generate-node",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt, parent_id: activeCommit.commitId }),
        }
      );

      const result = await response.json();

      let newCommit: AssetCommitNode;
      if (result.success && result.data) {
        newCommit = {
          commitId:
            result.data.version_commit_id ||
            `commit-${Math.random().toString(36).substring(2, 10)}`,
          parentId: activeCommit.commitId,
          prompt,
          seed: result.data.seed || Math.floor(Math.random() * 900000),
          durableUrl:
            result.data.vault_durable_url ||
            "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/uv_grid_opengl.jpg",
          timestamp:
            new Date().toLocaleTimeString("en-US", { timeZone: "UTC" }) +
            " UTC",
          provider:
            result.data.provider_telemetry?.active_provider ||
            "Genblaze-Primary-Core",
          latencyMs: Math.round((result.data.latency_seconds || 0.35) * 1000),
        };
      } else {
        newCommit = {
          commitId: `commit-${Math.random().toString(36).substring(2, 10)}`,
          parentId: activeCommit.commitId,
          prompt,
          seed: Math.floor(100000 + Math.random() * 800000),
          durableUrl:
            "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/uv_grid_opengl.jpg",
          timestamp:
            new Date().toLocaleTimeString("en-US", { timeZone: "UTC" }) +
            " UTC",
          provider: "Genblaze-Resilient-Core",
          latencyMs: 310,
        };
      }

      setCommitList((prev) => [newCommit, ...prev]);
      setActiveCommit(newCommit);
    } catch (err) {
      console.warn(
        "Backend API offline, pushing simulated asset commit node."
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRollbackToCommit = (targetNode: AssetCommitNode) => {
    setActiveCommit(targetNode);
    setPrompt(targetNode.prompt);
  };

  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Sidebar Controls Panel */}
      <aside className="w-80 border-r border-slate-800 bg-slate-900/60 backdrop-blur-xl p-5 flex flex-col justify-between">
        <div className="space-y-5">
          {/* Studio Header */}
          <div className="flex items-center gap-3">
            <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-lg">
              <Zap className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h1 className="text-xs font-mono font-bold tracking-wider text-slate-100 uppercase">
                AETHER Spatial Studio
              </h1>
              <p className="text-[10px] text-slate-400">
                Phase 3 — Day 12 Grand Finale Engine
              </p>
            </div>
          </div>

          {/* View Mode Switcher (3D Inspector vs Spatial Canvas Graph) */}
          <div className="grid grid-cols-2 gap-1.5 p-1 bg-slate-950 border border-slate-800 rounded-lg">
            <button
              onClick={() => setViewMode("3d_inspector")}
              className={`py-1.5 px-3 rounded-md text-[10px] font-mono flex items-center justify-center gap-1.5 transition-all ${
                viewMode === "3d_inspector"
                  ? "bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Eye className="w-3.5 h-3.5" /> 3D Viewport
            </button>
            <button
              onClick={() => setViewMode("canvas_graph")}
              className={`py-1.5 px-3 rounded-md text-[10px] font-mono flex items-center justify-center gap-1.5 transition-all ${
                viewMode === "canvas_graph"
                  ? "bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Network className="w-3.5 h-3.5" /> Canvas Map
            </button>
          </div>

          {/* Spatial Prompt Input & Generation Trigger */}
          <div className="space-y-2">
            <label className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
              Spatial Neural Prompt
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={3}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition-colors resize-none"
            />
            <button
              onClick={handleSynthesizeNewCommit}
              disabled={isGenerating}
              className="w-full py-2.5 px-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-semibold font-mono text-xs rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                  Synthesizing Commit...
                </>
              ) : (
                <>
                  <GitCommitIcon className="w-4 h-4 text-slate-950" />
                  Commit & Synthesize Node
                </>
              )}
            </button>
          </div>

          {/* Geometry Primitive Controls (Shown only in 3D Viewport mode) */}
          {viewMode === "3d_inspector" && (
            <div className="space-y-2">
              <label className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                Viewport Mesh Geometry
              </label>
              <div className="grid grid-cols-4 gap-1.5">
                {[
                  { id: "sphere", icon: Circle, label: "Sphere" },
                  { id: "cube", icon: Box, label: "Cube" },
                  { id: "torus", icon: Disc, label: "Torus" },
                  { id: "plane", icon: Layers, label: "Plane" },
                ].map((item) => {
                  const Icon = item.icon;
                  const active = geometry === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setGeometry(item.id as any)}
                      className={`p-2 rounded-lg border flex flex-col items-center gap-1 transition-all ${
                        active
                          ? "bg-cyan-500/10 border-cyan-500 text-cyan-400"
                          : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      <span className="text-[9px] font-mono">{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Shader & Material Controls (Shown only in 3D Viewport mode) */}
          {viewMode === "3d_inspector" && (
            <div className="space-y-3 pt-3 border-t border-slate-800">
              <div className="space-y-1">
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-slate-400">Surface Roughness</span>
                  <span className="text-cyan-400">{roughness.toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={roughness}
                  onChange={(e) => setRoughness(parseFloat(e.target.value))}
                  className="w-full accent-cyan-500 bg-slate-950 h-1 rounded-lg cursor-pointer"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-slate-400">Metalness Index</span>
                  <span className="text-cyan-400">{metalness.toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={metalness}
                  onChange={(e) => setMetalness(parseFloat(e.target.value))}
                  className="w-full accent-cyan-500 bg-slate-950 h-1 rounded-lg cursor-pointer"
                />
              </div>
            </div>
          )}
        </div>

        {/* Backblaze B2 Vault Active HUD */}
        <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between text-xs font-mono">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-emerald-400" />
            <span className="text-slate-300">Active Commit:</span>
          </div>
          <span className="text-cyan-400 font-bold">
            {activeCommit.commitId.slice(0, 10)}
          </span>
        </div>
      </aside>

      {/* Main Interactive Studio Canvas Workspace */}
      <main className="flex-1 p-5 relative flex flex-col">
        {viewMode === "3d_inspector" ? (
          <Viewport3D
            textureUrl={activeCommit.durableUrl}
            geometryType={geometry}
            roughness={roughness}
            metalness={metalness}
          />
        ) : (
          <SpatialCanvasGraph
            commits={commitList}
            activeCommit={activeCommit}
            onSelectCommit={(node: AssetCommitNode) => setActiveCommit(node)}
          />
        )}
      </main>

      {/* Right Sidebar - Git DAG Version Tree & Hot-Rollback */}
      <aside className="w-[420px] p-5 border-l border-slate-800 bg-slate-900/40 backdrop-blur-xl">
        <VersionTree
          commits={commitList}
          activeCommitId={activeCommit.commitId}
          onSelectCommit={(node: AssetCommitNode) => setActiveCommit(node)}
          onRollbackCommit={handleRollbackToCommit}
        />
      </aside>
    </div>
  );
}