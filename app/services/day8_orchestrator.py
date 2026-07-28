import time
import uuid
import json
import logging
from app.services.resilient_orchestrator import day6_pipeline
from app.services.telemetry_sink import telemetry_sink
from app.services.analytics_engine import analytics_engine
from app.services.b2_service import b2_vault

logger = logging.getLogger("Day8Orchestrator")

class Day8AnalyticsPipeline:
    async def process_with_realtime_analytics(self, prompt: str, parent_id: str = "root") -> dict:
        start_time = time.time()
        trace_id = f"tr-day8-{uuid.uuid4().hex[:10]}"

        # Step 1: Execute Resilient Primary / Fallback Call
        result = await day6_pipeline.generate_resilient_asset(
            prompt=prompt, 
            parent_id=parent_id
        )

        total_latency_ms = (time.time() - start_time) * 1000.0
        provider_used = result["provider_telemetry"]["active_provider"]
        fallback_active = result["provider_telemetry"]["fallback_triggered"]
        circuit_state = result["provider_telemetry"]["circuit_breaker_state"]["state"]

        # Step 2: Process Real-time Statistical Profiling & Anomaly Detection
        analytics_result = analytics_engine.push_metric(
            latency_ms=total_latency_ms,
            is_fallback=fallback_active,
            status_code=200
        )

        # Step 3: Non-blocking Telemetry Record with Statistical Diagnostics
        await telemetry_sink.record_execution_metric(
            trace_id=trace_id,
            prompt=prompt,
            provider=provider_used,
            fallback_used=fallback_active,
            latency_ms=total_latency_ms,
            status_code=200,
            circuit_state=circuit_state,
            custom_metadata={
                "analytics_diagnostics": analytics_result,
                "version_commit_id": result.get("version_commit_id", "N/A")
            }
        )

        # Attach analytics diagnostic packet to final payload
        result["trace_id"] = trace_id
        result["realtime_analytics"] = analytics_result
        return result

    def sync_daily_summary_to_b2(self) -> str:
        """Flushes aggregated statistical summary manifest into Backblaze B2 Bucket."""
        summary = analytics_engine.generate_aggregated_audit_summary()
        json_bytes = json.dumps(summary, indent=2).encode('utf-8')
        
        file_name = f"telemetry_analytics/daily_health_summary_{int(time.time())}.json"
        
        file_info = b2_vault.bucket.upload_bytes(
            data_bytes=json_bytes,
            file_name=file_name,
            content_type="application/json",
            file_infos={"X-Bz-Info-Type": "daily_statistical_health_summary"}
        )
        
        return b2_vault.b2_api.get_download_url_for_file_name(
            bucket_name=b2_vault.bucket.name,
            file_name=file_info.file_name
        )

day8_pipeline = Day8AnalyticsPipeline()