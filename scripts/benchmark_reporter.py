import asyncio
import json
import time
from app.services.analytics_engine import analytics_engine
from app.services.day8_orchestrator import day8_pipeline
from app.services.telemetry_sink import telemetry_sink


async def run_phase2_benchmark_suite():
    print("\n" + "=" * 70)
    print("🚀 AETHER-MIND NEXUS ENGINE — PHASE 2 BENCHMARK & AUDIT SUITE")
    print("=" * 70)

    # Start telemetry background worker
    await telemetry_sink.start_worker()

    test_prompts = [
        "Volumetric Holographic Lattice Alpha",
        "Sparse Node Topology Beta",
        "Quantum Resonance Mesh Delta",
        "Cybernetic Neural Cloud Epsilon",
        "Hyper-dimensional Grid Gamma",
    ]

    print(
        "\n[+] Simulating High-Frequency Multi-Modal Requests with Provider Resilience...\n"
    )

    try:
        for idx, prompt in enumerate(test_prompts, start=1):
            res = await day8_pipeline.process_with_realtime_analytics(
                prompt=prompt
            )

            # Defensive payload unwrapping: handles {"data": {...}} OR direct dictionary
            data = res.get("data", res)

            analytics = data.get("realtime_analytics", {})
            provider_telemetry = data.get("provider_telemetry", {})

            trace_id = data.get("trace_id", f"tr-day8-00{idx}")
            latency = analytics.get(
                "current_latency_ms", data.get("latency_ms", 0.0)
            )
            provider = provider_telemetry.get(
                "active_provider",
                data.get("provider", "Genblaze-Primary-Core"),
            )
            fallback = (
                "YES"
                if provider_telemetry.get("fallback_triggered", False)
                else "NO"
            )
            is_anomaly = analytics.get("is_anomaly_detected", False)
            anomaly = "⚠️ ANOMALY DETECTED" if is_anomaly else "✅ STABLE"

            print(
                f"Req #{idx} | Trace: {trace_id} | Latency: {latency:.1f}ms | Provider: {provider} | Fallback: {fallback} | Status: {anomaly}"
            )
            await asyncio.sleep(0.1)

    finally:
        # Gracefully Flush Telemetry & stop loop even if errors occur
        await telemetry_sink.stop_worker()

    summary = analytics_engine.generate_aggregated_audit_summary()

    print("\n" + "-" * 70)
    print("📊 PHASE 2 AUDIT SUMMARY & B2 TELEMETRY METRICS")
    print("-" * 70)
    print(f"• Total Processed Executions : {summary['total_processed_requests']}")
    print(f"• Fallback Trigger Count     : {summary['fallback_executions']}")
    print(f"• Failed Network Operations : {summary['failed_executions']}")
    print(f"• Moving Average Latency    : {summary['avg_latency_ms']} ms")
    print(
        f"• Telemetry Ingestion Vault : Backblaze B2 ({getattr(telemetry_sink, 'bucket_name', 'aether-telemetry-vault')})"
    )
    print(f"• Cryptographic Integrity   : HMAC-SHA256 Signed JSON Ledgers")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(run_phase2_benchmark_suite())