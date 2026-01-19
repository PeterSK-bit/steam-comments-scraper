from config.exceptions import ConfigError

class EnvConfig:
    REQUIRED = ("steam_url",)
    OPTIONAL = ("steamLoginSecure", "sessionid", "MAX_PAGINATION_DEPTH")

    def __init__(self, path: str = "config/.env") -> None:
        self._path = path
        self._vars = self._load_env()
        self._normalize_vars()
    
    def _load_env(self) -> dict:
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
            return env_vars
        except FileNotFoundError:
            print("WARNING: .env file not found, program will run in restricted mode.")
            return {}
        except Exception as e:
            print(f"WARNING: Failed to read .env file, program will run in restricted mode.")
            return {}
    
    def _normalize_vars(self) -> None:
        for key in self.REQUIRED:
            if not self._vars.get(key):
                raise ConfigError(f"Missing required config: {key}")

        self._cookies_enabled = all(self._vars.get(k) for k in ("steamLoginSecure", "sessionid"))

        raw = self._vars.get("MAX_PAGINATION_DEPTH", "100")

        try:
            value = int(raw)
        except (ValueError, TypeError):
            value = 100

        self._vars["MAX_PAGINATION_DEPTH"] = value


    @property
    def steam_url(self) -> str:
        return self._vars.get("steam_url", "")
    
    @property
    def steam_login_secure(self) -> str:
        return self._vars.get("steamLoginSecure", "")
    
    @property
    def session_id(self) -> str:
        return self._vars.get("sessionid", "")
    
    @property
    def max_pagination_depth(self) -> int:
        return self._vars.get("MAX_PAGINATION_DEPTH", 100)
    
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