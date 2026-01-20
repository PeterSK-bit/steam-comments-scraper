from config.exceptions import ConfigError, EnvFileNotFound, EnvLoadError

class EnvConfig:
    REQUIRED = ("steam_url",)
    OPTIONAL = ("steamLoginSecure", "sessionid", "MAX_PAGINATION_DEPTH", "request_delay_ms")

    def __init__(self, path: str = "config/.env") -> None:
        self._path = path
        self._vars = {}
    
    def _load_env(self) -> None:
        env_vars = {}

        try:
            with open(self._path) as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#") or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    env_vars[key] = value
            self._vars = env_vars
        except FileNotFoundError as e:
            raise EnvFileNotFound(f"Env file not found at path: {self._path}") from e
        except Exception as e:
            raise EnvLoadError(f"Failed to load env file: {self._path}") from e
    
    def _normalize_vars(self) -> None:
        for key in self.REQUIRED:
            if not self._vars.get(key):
                raise ConfigError(f"Missing required config: {key}")

        self._cookies_enabled = all(self._vars.get(k) for k in ("steamLoginSecure", "sessionid"))
        self._vars["MAX_PAGINATION_DEPTH"] = self._normalize_int("MAX_PAGINATION_DEPTH", 100)
        self._vars["request_delay_ms"] = self._normalize_int("request_delay_ms", 0)

    def _normalize_int(self, key: str, default: int) -> int:
        raw = self._vars.get(key, default)

        try:
            value = int(raw)
        except (ValueError, TypeError):
            value = default

        return value

    @property
    def steam_url(self) -> str:
        return self._vars.get("steam_url", "")

    @steam_url.setter
    def steam_url(self, value: str) -> None:
        if not value:
            raise ConfigError("steam_url cannot be empty.")
        self._vars["steam_url"] = value
    
    @property
    def steam_login_secure(self) -> str:
        return self._vars.get("steamLoginSecure", "")
    
    @steam_login_secure.setter
    def steam_login_secure(self, value: str) -> None:
        if not value:
            raise ConfigError("steamLoginSecure cannot be empty.")
        self._vars["steamLoginSecure"] = value
    
    @property
    def session_id(self) -> str:
        return self._vars.get("sessionid", "")
    
    @session_id.setter
    def session_id(self, value: str) -> None:
        if not value:
            raise ConfigError("sessionid cannot be empty.")
        self._vars["sessionid"] = value
    
    @property
    def max_pagination_depth(self) -> int:
        return self._vars.get("MAX_PAGINATION_DEPTH", 100)

    @max_pagination_depth.setter
    def max_pagination_depth(self, value: int) -> None:
        if not isinstance(value, int):
            raise ConfigError("MAX_PAGINATION_DEPTH must be an integer.")
        
        if value <= 0:
            raise ConfigError("MAX_PAGINATION_DEPTH must be a positive integer.")
        
        self._vars["MAX_PAGINATION_DEPTH"] = value
    
    @property
    def request_delay_ms(self) -> int:
        return self._vars.get("request_delay_ms", 0)
    
    @request_delay_ms.setter
    def request_delay_ms(self, value: int) -> None:
        if not isinstance(value, int):
            raise ConfigError("request_delay_ms must be an integer.")
        
        if value < 0:
            raise ConfigError("request_delay_ms cannot be negative.")
        
        self._vars["request_delay_ms"] = value

    @property
    def cookies_enabled(self) -> bool:
        return self._cookies_enabled
    
    @property
    def cookies(self) -> dict | None:
        if not self._cookies_enabled:
            return None
        return {
            'steamLoginSecure': self.steam_login_secure,
            'sessionid': self.session_id
        }