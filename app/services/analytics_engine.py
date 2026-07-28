import math
import time
from typing import List, Dict, Any

class StatisticalAnomalyEngine:
    def __init__(self, window_size: int = 50, target_latency_ms: float = 200.0):
        self.window_size = window_size
        self.target_latency_ms = target_latency_ms
        self.latency_window: List[float] = []
        self.total_requests = 0
        self.failed_requests = 0
        self.fallback_count = 0

    def push_metric(self, latency_ms: float, is_fallback: bool, status_code: int) -> Dict[str, Any]:
        self.total_requests += 1
        if status_code != 200:
            self.failed_requests += 1
        if is_fallback:
            self.fallback_count += 1

        self.latency_window.append(latency_ms)
        if len(self.latency_window) > self.window_size:
            self.latency_window.pop(0)

        n = len(self.latency_window)
        mean = sum(self.latency_window) / n if n > 0 else 0.0
        
        # Sample Variance (Bessel's correction if n > 1)
        variance = sum((x - mean) ** 2 for x in self.latency_window) / (n - 1 if n > 1 else 1)
        std_dev = math.sqrt(variance)

        # Statistical Z-Score (Avoid Division by Zero)
        z_score = 0.0
        if std_dev > 0.001:
            z_score = (latency_ms - mean) / std_dev
        elif n == 1 and latency_ms > (self.target_latency_ms * 2):
            z_score = 3.0  # Cold start anomaly protection

        is_anomaly = z_score > 2.5  # Anomaly Trigger Threshold

        # Dynamic Provider Health Index Calculation (0 - 100)
        success_rate = ((self.total_requests - self.failed_requests) / self.total_requests) * 100.0
        fallback_ratio = (self.fallback_count / self.total_requests) * 100.0
        
        # Latency Score: 30 pts max if mean <= target_latency_ms
        latency_ratio = mean / self.target_latency_ms if self.target_latency_ms > 0 else 1.0
        latency_score = max(0.0, 30.0 * (1.0 - max(0.0, latency_ratio - 1.0)))

        # Weighted Health Matrix Component: Success (60%) + Latency (30%) + Native Execution (10%)
        health_score = round(
            (success_rate * 0.60) + 
            latency_score + 
            (max(0.0, 10.0 - (fallback_ratio * 0.1))), 
            2
        )

        return {
            "current_latency_ms": round(latency_ms, 2),
            "rolling_mean_ms": round(mean, 2),
            "rolling_std_dev": round(std_dev, 2),
            "z_score": round(z_score, 3),
            "is_anomaly_detected": is_anomaly,
            "provider_health_index": min(100.0, health_score),
            "window_sample_count": n
        }

    def generate_aggregated_audit_summary(self) -> Dict[str, Any]:
        """Generates periodic aggregated health manifest for B2 Vaulting."""
        n = len(self.latency_window)
        mean = sum(self.latency_window) / n if n > 0 else 0.0
        return {
            "summary_schema_version": "1.0.0-Day8",
            "timestamp": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "total_processed_requests": self.total_requests,
            "fallback_executions": self.fallback_count,
            "failed_executions": self.failed_requests,
            "avg_latency_ms": round(mean, 2),
            "latency_window_samples": self.latency_window[-10:] if n > 0 else []
        }

analytics_engine = StatisticalAnomalyEngine(window_size=50, target_latency_ms=300.0)