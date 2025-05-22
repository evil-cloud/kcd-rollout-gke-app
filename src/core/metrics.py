from prometheus_client import Counter, Histogram, Gauge

HTTP_CLIENT_EXTERNAL_API_REQUESTS_TOTAL = Counter(
    'http_client_external_api_requests_total',
    'Total number of HTTP client requests made to the external API.',
    ['status']
)


HTTP_CLIENT_EXTERNAL_API_REQUEST_DURATION_SECONDS = Histogram(
    'http_client_external_api_request_duration_seconds',
    'Histogram of external API request duration in seconds.',
    ['status']
)

CIRCUIT_BREAKER_EXTERNAL_API_STATE = Gauge(
    'circuit_breaker_external_api_state',
    'State of the external API circuit breaker (0: Closed, 1: Open, 2: Half-Open).'
)