import requests
from fastapi import HTTPException
import pybreaker
from timeit import default_timer as timer
from core.metrics import (
    HTTP_CLIENT_EXTERNAL_API_REQUESTS_TOTAL,
    HTTP_CLIENT_EXTERNAL_API_REQUEST_DURATION_SECONDS,
    CIRCUIT_BREAKER_EXTERNAL_API_STATE
)
from core.config import settings
from pybreaker import CircuitBreakerListener

class CircuitBreakerMetricsListener(CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        state_value = 0
        if new_state.name == 'open':
            state_value = 1
        elif new_state.name == 'half-open':
            state_value = 2

        CIRCUIT_BREAKER_EXTERNAL_API_STATE.set(state_value)
        print(f"Circuit Breaker '{cb.name if hasattr(cb, 'name') else 'unknown'}' state changed from {old_state.name} to {new_state.name}. Metric value set to {state_value}")

external_api_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=10,
    exclude=[HTTPException],
    listeners=[CircuitBreakerMetricsListener()]
)

class ExternalAPI:
    @external_api_breaker
    def fetch_data(self):
        start_time = timer()
        try:
            response = requests.get(settings.EXTERNAL_API_URL, timeout=5)
            response.raise_for_status()

            HTTP_CLIENT_EXTERNAL_API_REQUESTS_TOTAL.labels(status='success').inc()
            end_time = timer()
            duration = end_time - start_time
            HTTP_CLIENT_EXTERNAL_API_REQUEST_DURATION_SECONDS.labels(status='success').observe(duration)

            return response.json()

        except requests.exceptions.RequestException as e:
            HTTP_CLIENT_EXTERNAL_API_REQUESTS_TOTAL.labels(status='failure').inc()
            end_time = timer()
            duration = end_time - start_time
            HTTP_CLIENT_EXTERNAL_API_REQUEST_DURATION_SECONDS.labels(status='failure').observe(duration)

            raise HTTPException(status_code=503, detail=f"Fallo en la API externa: {str(e)}")

process_data = ExternalAPI().fetch_data

CIRCUIT_BREAKER_EXTERNAL_API_STATE.set(0)