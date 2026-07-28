import asyncio
import time
from app.services.analytics_engine import analytics_engine

async def run_day8_simulation():
    print("=" * 60)
    print("🔥 STARTING DAY 8 REAL-TIME ANOMALY DETECTION TEST")
    print("=" * 60)

    # 1. Simulate Normal Baseline Latencies (around 100ms - 120ms)
    print("\n1. Seeding baseline latency stream (15 normal requests)...")
    for i in range(15):
        latency = 100.0 + (i % 3) * 5.0  # 100ms, 105ms, 110ms
        res = analytics_engine.push_metric(latency_ms=latency, is_fallback=False, status_code=200)
        print(f"Req #{i+1:02d} | Latency: {latency:.1f}ms | Mean: {res['rolling_mean_ms']}ms | Z-Score: {res['z_score']} | Anomaly: {res['is_anomaly_detected']}")

    # 2. Inject Artificial Latency Spike (500ms)
    print("\n2. Injecting sudden Latency Spike (500ms)...")
    spike_latency = 500.0
    spike_res = analytics_engine.push_metric(latency_ms=spike_latency, is_fallback=True, status_code=200)
    
    print("-" * 60)
    print(f"🚨 SPIKE RESULT:")
    print(f"   Current Latency: {spike_res['current_latency_ms']} ms")
    print(f"   Rolling Mean:    {spike_res['rolling_mean_ms']} ms")
    print(f"   Std Deviation:   {spike_res['rolling_std_dev']}")
    print(f"   Z-Score:         {spike_res['z_score']}")
    print(f"   ANOMALY DETECTED: {spike_res['is_anomaly_detected']}")
    print(f"   Health Index:    {spike_res['provider_health_index']}%")
    print("-" * 60)

    if spike_res['is_anomaly_detected']:
        print("✅ SUCCESS: Z-Score Outlier Engine successfully caught the spike (Z > 2.5)!")
    else:
        print("⚠️ WARNING: Spike did not clear threshold Z > 2.5.")

if __name__ == "__main__":
    asyncio.run(run_day8_simulation())