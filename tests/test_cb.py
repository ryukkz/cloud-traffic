from  gateway.circuit_breaker import CircuitBreaker
import time

cb = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

print(cb.state)

cb.record_failure()
cb.record_failure()
cb.record_failure()

print(cb.state)

print(cb.allow_request())  # Should be False

time.sleep(5)

print(cb.allow_request())  # Should be True
print(cb.state)            # Should be half_open

cb.record_success()

print(cb.state)            # Should be closed