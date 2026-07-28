import pytest
import asyncio
import time
from app.services.circuit_breaker import AdaptiveCircuitBreaker, CircuitState
from app.services.analytics_engine import StatisticalAnomalyEngine
from app.services.telemetry_sink import Day7AsyncTelemetrySink

@pytest.mark.asyncio
async def test_circuit_breaker_state_machine():
    cb = AdaptiveCircuitBreaker(failure_threshold=2, recovery_timeout_sec=0.5)
    assert cb.state == CircuitState.CLOSED
    
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.can_execute() is False
    
    # Wait for recovery timeout to verify HALF_OPEN transition
    await asyncio.sleep(0.6)
    assert cb.can_execute() is True
    assert cb.state == CircuitState.HALF_OPEN
    
    cb.record_success()
    assert cb.state == CircuitState.CLOSED

def test_statistical_z_score_anomaly_detection():
    engine = StatisticalAnomalyEngine(window_size=10)
    
    # Feed stable baseline latencies (~100ms)
    for _ in range(10):
        engine.push_metric(latency_ms=100.0, is_fallback=False, status_code=200)
    
    # Simulate sudden 1500ms latency spike
    result = engine.push_metric(latency_ms=1500.0, is_fallback=True, status_code=200)
    
    assert result["is_anomaly_detected"] is True, "Z-Score Engine must flag 1500ms spike as anomaly!"
    assert result["z_score"] > 2.5, "Z-Score must exceed 2.5 threshold on extreme latency spikes."

@pytest.mark.asyncio
async def test_telemetry_async_queue_drain():
    sink = Day7AsyncTelemetrySink()
    await sink.start_worker()
    
    # Queue test telemetry event
    await sink.record_execution_metric(
        trace_id="test-trace-999",
        prompt="Integration Test Vector",
        provider="Genblaze-Test",
        fallback_used=False,
        latency_ms=120.5,
        status_code=200,
        circuit_state="CLOSED"
    )
    
    assert sink._queue.qsize() == 1
    await sink.stop_worker()
    assert sink._queue.qsize() == 0, "Queue must gracefully drain all logs before shutdown."