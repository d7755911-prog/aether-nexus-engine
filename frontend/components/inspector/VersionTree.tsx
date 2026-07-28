"use client";

import React from "react";
import {
  GitCommit,
  GitBranch,
  RotateCcw,
  CheckCircle2,
  Hash,
  Cpu,
  Clock,
} from "lucide-react";

export interface AssetCommitNode {
  commitId: string;
  parentId: string | null;
  prompt: string;
  seed: number;
  durableUrl: string;
  timestamp: string;
  provider: string;
  latencyMs: number;
  branchName?: string;
}

export interface VersionTreeProps {
  commits: AssetCommitNode[];
  activeCommitId: string;
  onSelectCommit: (node: AssetCommitNode) => void;
  onRollbackCommit: (node: AssetCommitNode) => void;
}

export default function VersionTree({
  commits,
  activeCommitId,
  onSelectCommit,
  onRollbackCommit,
}: VersionTreeProps) {
  return (
    <div className="w-full h-full bg-slate-950/90 border border-slate-800 rounded-xl p-4 flex flex-col justify-between backdrop-blur-xl shadow-2xl">
      {/* Header Bar */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-cyan-400" />
          <h2 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
            Spatial Asset Lineage Tree (DAG)
          </h2>
        </div>
        <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 border border-cyan-500/30 px-2 py-0.5 rounded-full">
          {commits.length} Commits Vaulted
        </span>
      </div>

      {/* Interactive Visual Graph Nodes Scroll Area */}
      <div className="flex-1 overflow-y-auto my-4 pr-2 space-y-3 custom-scrollbar">
        {commits.map((node, index) => {
          const isActive = node.commitId === activeCommitId;
          const hasParent = node.parentId !== null && node.parentId !== "root";

          return (
            <div
              key={node.commitId}
              className="relative flex items-start gap-3 group"
            >
              {/* Vertical Git Branch Line Visualizer */}
              {index !== commits.length - 1 && (
                <div className="absolute left-[15px] top-[32px] w-[2px] h-[calc(100%+12px)] bg-slate-800 group-hover:bg-cyan-500/40 transition-colors" />
              )}

              {/* Commit Circle Marker */}
              <button
                onClick={() => onSelectCommit(node)}
                className={`relative z-10 mt-1 w-8 h-8 rounded-full flex items-center justify-center border transition-all ${
                  isActive
                    ? "bg-cyan-500 border-cyan-300 text-slate-950 shadow-lg shadow-cyan-500/30 ring-2 ring-cyan-500/50"
                    : "bg-slate-900 border-slate-700 text-slate-400 hover:border-cyan-500 hover:text-cyan-400"
                }`}
              >
                {isActive ? (
                  <CheckCircle2 className="w-4 h-4" />
                ) : (
                  <GitCommit className="w-4 h-4" />
                )}
              </button>

              {/* Commit Content Card */}
              <div
                onClick={() => onSelectCommit(node)}
                className={`flex-1 p-3 rounded-lg border transition-all cursor-pointer ${
                  isActive
                    ? "bg-slate-900/90 border-cyan-500/60 shadow-md shadow-cyan-950/40"
                    : "bg-slate-950/60 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/40"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-semibold text-cyan-400">
                      {node.commitId}
                    </span>
                    {hasParent && (
                      <span className="text-[10px] font-mono text-slate-500 flex items-center gap-1">
                        <Hash className="w-3 h-3" /> parent:{" "}
                        {node.parentId?.slice(0, 8)}
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-500" /> {node.timestamp}
                  </span>
                </div>

                <p className="text-xs text-slate-300 line-clamp-1 my-1.5 font-sans">
                  "{node.prompt}"
                </p>

                {/* Metadata Row */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[10px] font-mono text-slate-400">
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Cpu className="w-3 h-3 text-slate-500" /> {node.provider}
                    </span>
                    <span>{node.latencyMs}ms</span>
                  </div>

                  {/* Rollback Trigger Button */}
                  {!isActive && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onRollbackCommit(node);
                      }}
                      className="flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 bg-cyan-500/10 border border-cyan-500/30 hover:bg-cyan-500/20 px-2 py-0.5 rounded transition-all"
                    >
                      <RotateCcw className="w-3 h-3" /> Rollback
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer Info */}
      <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px] font-mono text-slate-500">
        <span>Git SHA-256 Provenance Ledger Active</span>
        <span className="text-emerald-400">Backblaze B2 Vault Sync</span>
      </div>
    </div>
  );
}