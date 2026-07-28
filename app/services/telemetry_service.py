import time
import hmac
import hashlib
import json
import psutil
from typing import Dict, Any

class TelemetryAuditEngine:
    def __init__(self, secret_key: str = "AETHER_NEXUS_SECRET_2026"):
        self.secret_key = secret_key.encode('utf-8')

    def capture_system_snapshot(self) -> Dict[str, Any]:
        """Captures host compute metrics without external dependencies."""
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        return {
            "cpu_utilization_pct": cpu_usage,
            "ram_used_mb": round(memory.used / (1024 * 1024), 2),
            "ram_available_mb": round(memory.available / (1024 * 1024), 2)
        }

    def generate_hmac_signature(self, payload_bytes: bytes) -> str:
        """Generates cryptographically secure signature for B2 payload verification."""
        return hmac.new(self.secret_key, payload_bytes, hashlib.sha256).hexdigest()

    def build_audit_telemetry(
        self,
        commit_id: str,
        prompt: str,
        seed: int,
        latency: float,
        resilience_data: Dict[str, Any],
        asset_manifest_urls: Dict[str, Any]
    ) -> Dict[str, Any]:
        timestamp = time.time_ns()
        system_stats = self.capture_system_snapshot()

        raw_telemetry = {
            "telemetry_id": f"telemetry-{timestamp}",
            "associated_commit_id": commit_id,
            "timestamp_ns": timestamp,
            "execution_latency_sec": latency,
            "resilience_telemetry": resilience_data,
            "host_health": system_stats,
            "prompt_hash": hashlib.sha256(prompt.encode('utf-8')).hexdigest(),
            "asset_distribution": asset_manifest_urls
        }

        # Convert to deterministic JSON for cryptographic signing
        serialized_data = json.dumps(raw_telemetry, sort_keys=True).encode('utf-8')
        signature = self.generate_hmac_signature(serialized_data)

        raw_telemetry["cryptographic_signature"] = signature
        raw_telemetry["signature_algorithm"] = "HMAC-SHA256"

        return raw_telemetry

telemetry_engine = TelemetryAuditEngine()