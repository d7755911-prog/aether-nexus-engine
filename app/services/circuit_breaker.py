import time
from enum import Enum
from typing import Dict, Any

class CircuitState(Enum):
    CLOSED = "CLOSED"        # Normal Operation (Primary Operational)
    OPEN = "OPEN"            # Provider Down (Instant Fallback Route)
    HALF_OPEN = "HALF_OPEN"  # Testing Recovery

class CircuitBreakerOpenException(Exception):
    """Raised when the circuit is OPEN and requests should fail-fast to fallback."""
    pass

class AdaptiveCircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout_sec: float = 15.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_state_change = time.time()

    def record_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.last_state_change = time.time()

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has elapsed to attempt Half-Open test
            if (time.time() - self.last_state_change) > self.recovery_timeout_sec:
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = time.time()
                return True
            return False

        # HALF_OPEN state allows single trial request
        return True

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "last_state_change_timestamp": self.last_state_change
        }