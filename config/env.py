import config.exceptions as config

class EnvConfig:
    REQUIRED = ("steam_url",)
    OPTIONAL = (
        "steamLoginSecure", "sessionid", "MAX_PAGINATION_DEPTH", "request_delay_ms", "print_config", "dry_run"
        )

    def __init__(self, path: str = "config/.env") -> None:
        self._path: str = path
        self._vars: dict = { key: None for key in self.REQUIRED + self.OPTIONAL }
        self._cookies_enabled: bool = False
    
    def _load_env(self) -> None:
        if not self._path:
            raise config.EnvFilePathNotProvided("Environment file path not provided. Use CLI arg to specify env file path.")
        
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
            raise config.EnvFileNotFound(f"Env file not found at path: {self._path}") from e
        except Exception as e:
            raise config.EnvLoadError(f"Failed to load env file: {self._path}") from e
    
    def _normalize_vars(self) -> None:
        for key in self.REQUIRED:
            if not self._vars.get(key):
                raise config.ConfigError(f"Missing required config: {key}")

        self._cookies_enabled = all(self._vars.get(k) for k in ("steamLoginSecure", "sessionid"))
        self._vars["MAX_PAGINATION_DEPTH"] = self._normalize_int("MAX_PAGINATION_DEPTH", 100)
        self._vars["request_delay_ms"] = self._normalize_int("request_delay_ms", 0)
        self._vars["print_config"] = self._normalize_bool("print_config", False)
        self._vars["dry_run"] = self._normalize_bool("dry_run", False)

    def _normalize_int(self, key: str, default: int) -> int:
        raw = self._vars.get(key, default)

        try:
            value = int(raw)
        except (ValueError, TypeError):
            value = default

        return value

    def _normalize_bool(self, key: str, default: bool) -> bool:
        raw = self._vars.get(key, default)

        if isinstance(raw, bool):
            return raw
        
        if isinstance(raw, str):
            return raw.lower() in ("1", "true", "yes", "on")
        
        return default

    @property
    def steam_url(self) -> str:
        return self._vars.get("steam_url", "")

    @steam_url.setter
    def steam_url(self, value: str) -> None:
        if isinstance(value, str) or value == None:
            raise config.ConfigError("steam_url must be a string or None.")
        self._vars["steam_url"] = value
    
    @property
    def steam_login_secure(self) -> str:
        return self._vars.get("steamLoginSecure", "")
    
    @steam_login_secure.setter
    def steam_login_secure(self, value: str) -> None:
        if isinstance(value, str) or value == None:
            raise config.ConfigError("steamLoginSecure must be a string or None.")
        self._vars["steamLoginSecure"] = value
    
    @property
    def session_id(self) -> str:
        return self._vars.get("sessionid", "")
    
    @session_id.setter
    def session_id(self, value: str) -> None:
        if isinstance(value, str) or value == None:
            raise config.ConfigError("sessionid must be a string or None.")
        self._vars["sessionid"] = value
    
    @property
    def max_pagination_depth(self) -> int:
        return self._vars.get("MAX_PAGINATION_DEPTH", 100)

    @max_pagination_depth.setter
    def max_pagination_depth(self, value: int) -> None:
        if not isinstance(value, int):
            raise ConfigError("MAX_PAGINATION_DEPTH must be an integer.")
        
        if value <= 0:
            raise config.ConfigError("MAX_PAGINATION_DEPTH must be a positive integer.")
        
        self._vars["MAX_PAGINATION_DEPTH"] = value
    
    @property
    def request_delay_ms(self) -> int:
        return self._vars.get("request_delay_ms", 0)
    
    @request_delay_ms.setter
    def request_delay_ms(self, value: int) -> None:
        if not isinstance(value, int):
            raise ConfigError("request_delay_ms must be an integer.")
        
        if value < 0:
            raise config.ConfigError("request_delay_ms cannot be negative.")
        
        self._vars["request_delay_ms"] = value
    
    @property
    def print_config(self) -> bool:
        return self._vars.get("print_config", False)
    
    @print_config.setter
    def print_config(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise config.ConfigError("print_config must be a boolean.")
        self._vars["print_config"] = value
    
    @property
    def dry_run(self) -> bool:
        return self._vars.get("dry_run", False)
    
    @dry_run.setter
    def dry_run(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise config.ConfigError("dry_run must be a boolean.")
        self._vars["dry_run"] = value

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