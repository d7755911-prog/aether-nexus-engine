import asyncio
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

from app.services.b2_service import b2_vault


class Day7AsyncTelemetrySink:

    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._worker_task: Optional[asyncio.Task] = None
        self._is_running = False
        self.secret_key = b"AETHER_NEXUS_HMAC_SECRET_2026"

    def _generate_telemetry_signature(self, payload_str: str) -> str:
        """Generates HMAC-SHA256 signature for telemetry log integrity verification."""
        return hmac.new(
            self.secret_key, payload_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    async def start_worker(self):
        """Starts background non-blocking telemetry ingestion worker loop."""
        if not self._is_running:
            self._is_running = True
            self._worker_task = asyncio.create_task(
                self._telemetry_ingestion_loop()
            )

    async def stop_worker(self):
        """Gracefully drains the queue before server shutdown."""
        self._is_running = False
        if self._worker_task:
            await self._queue.join()
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def record_execution_metric(
        self,
        trace_id: str,
        prompt: str,
        provider: str,
        fallback_used: bool,
        latency_ms: float,
        status_code: int,
        circuit_state: str,
        custom_metadata: Optional[Dict[str, Any]] = None,
    ):
        """Non-blocking method called by main pipeline to queue execution logs."""
        telemetry_event = {
            "telemetry_schema_version": "2.0.0-Day7",
            "trace_id": trace_id,
            "timestamp_utc": time.time(),
            "formatted_time": time.strftime(
                "%Y-%m-%d %H:%M:%S UTC", time.gmtime()
            ),
            "execution_metrics": {
                "total_latency_ms": round(latency_ms, 3),
                "active_provider": provider,
                "fallback_triggered": fallback_used,
                "circuit_breaker_state": circuit_state,
                "http_status_code": status_code,
            },
            "request_payload_digest": {
                "prompt_length": len(prompt),
                "prompt_sha256": hashlib.sha256(
                    prompt.encode("utf-8")
                ).hexdigest(),
            },
            "system_node_telemetry": custom_metadata
            or {
                "engine_version": "AETHER-MIND-v6",
                "environment": "production-hackathon-node",
            },
        }

        # Add HMAC signature to log payload
        raw_payload_str = json.dumps(telemetry_event, sort_keys=True)
        telemetry_event["cryptographic_signature"] = (
            self._generate_telemetry_signature(raw_payload_str)
        )

        # Push to async queue without blocking primary API response
        await self._queue.put(telemetry_event)

    async def _telemetry_ingestion_loop(self):
        """Background worker that continuously streams JSON telemetry logs to Backblaze B2."""
        while self._is_running or not self._queue.empty():
            try:
                try:
                    event = await asyncio.wait_for(
                        self._queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                trace_id = event["trace_id"]
                file_name = f"telemetry_logs/{time.strftime('%Y-%m-%d')}/{trace_id}_metric.json"
                json_bytes = json.dumps(event, indent=2).encode("utf-8")

                # ✅ FIXED: Using 'file_info' (renamed from deprecated 'file_infos')
                b2_vault.bucket.upload_bytes(
                    data_bytes=json_bytes,
                    file_name=file_name,
                    content_type="application/json",
                    file_info={
                        "X-Bz-Info-Log-Type": "execution_telemetry",
                        "X-Bz-Info-Trace-ID": trace_id,
                        "X-Bz-Info-HMAC-Sig": event["cryptographic_signature"],
                    },
                )

                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Non-fatal telemetry ingest failure handling
                print(
                    f"[Day 7 Telemetry Sink Warning]: Non-fatal telemetry ingest delay: {str(e)}"
                )
                self._queue.task_done()
                await asyncio.sleep(0.5)


telemetry_sink = Day7AsyncTelemetrySink()