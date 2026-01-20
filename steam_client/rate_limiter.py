from time import sleep, monotonic

class RateLimiter:
    def __init__(self, min_interval_ms: int):
        self._min_interval = min_interval_ms / 1000
        self._last_call = 0.0

    def wait(self):
        now = monotonic()
        elapsed = now - self._last_call

        if elapsed < self._min_interval:
            sleep(self._min_interval - elapsed)

        self._last_call = monotonic()
