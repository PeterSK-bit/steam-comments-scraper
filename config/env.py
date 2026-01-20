from cli.config_print_mode import ConfigPrintMode

import config.exceptions as config

class EnvConfig:
    REQUIRED = ("steam_url",)
    OPTIONAL = (
        "steamLoginSecure", "sessionid", "MAX_PAGINATION_DEPTH", "request_delay_ms", "print_config_mode", "dry_run"
        )
    SENSITIVE_KEYS = ("steamLoginSecure", "sessionid")

    def __init__(self, path: str = "config/.env") -> None:
        self._path: str = path
        self._user_config: dict = { key: None for key in self.REQUIRED + self.OPTIONAL }
        self._cookies_enabled: bool = False

    def to_dict(self) -> dict:
        data = {
            "env_path": self._path,
            **self._user_config,
            "cookies_enabled": self._cookies_enabled
        }

        for k, v in self._user_config.items():
            if k == "print_config_mode":
                data[k] = v.value
            elif k in self.SENSITIVE_KEYS and self.print_config_mode == ConfigPrintMode.SAFE:
                data[k] = "*****"
            else:
                data[k] = v

        return data
    
    def apply_env(self) -> None:
        raw = self._load_env()

        for key, value in raw.items():
            self._apply_value(key, value)
        
        self._normalize_vars()


    def _load_env(self) -> dict[str, str]:
        if not self._path:
            raise config.EnvFilePathNotProvided("Environment file path not provided. Use CLI arg to specify env file path.")

        env: dict[str, str] = {}

        try:
            with open(self._path) as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#") or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip()

                    if key not in self.REQUIRED + self.OPTIONAL:
                        continue

                    env[key] = value.strip().strip('"').strip("'")

            return env
        except FileNotFoundError as e:
            raise config.EnvFileNotFound(f"Env file not found at path: {self._path}") from e
        except Exception as e:
            raise config.EnvLoadError(f"Failed to load env file: {self._path}") from e
    
    def _apply_value(self, key: str, raw: str) -> None:
        match key:
            case "steam_url":
                self.steam_url = raw

            case "steamLoginSecure":
                self.steam_login_secure = raw

            case "sessionid":
                self.session_id = raw

            case "MAX_PAGINATION_DEPTH":
                self.max_pagination_depth = int(raw)

            case "request_delay_ms":
                self.request_delay_ms = int(raw)

            case "print_config_mode":
                self.print_config_mode = ConfigPrintMode.parse(raw)

            case "dry_run":
                self.dry_run = raw.lower() in ("1", "true", "yes")

            case _:
                pass

    def _normalize_vars(self) -> None:
        for key in self.REQUIRED:
            if not self._user_config.get(key):
                raise config.ConfigError(f"Missing required config: {key}")

        self._cookies_enabled = all(self._user_config.get(k) for k in ("steamLoginSecure", "sessionid"))
        self._user_config["MAX_PAGINATION_DEPTH"] = self._normalize_int("MAX_PAGINATION_DEPTH", 100)
        self._user_config["request_delay_ms"] = self._normalize_int("request_delay_ms", 0)
        self._user_config["print_config_mode"] = self._normalize_print_mode("print_config_mode", ConfigPrintMode.NONE)
        self._user_config["dry_run"] = self._normalize_bool("dry_run", False)

    def _normalize_int(self, key: str, default: int) -> int:
        raw = self._user_config.get(key, default)

        try:
            value = int(raw)
        except (ValueError, TypeError):
            value = default

        return value

    def _normalize_bool(self, key: str, default: bool) -> bool:
        raw = self._user_config.get(key, default)

        if isinstance(raw, bool):
            return raw
        
        if isinstance(raw, str):
            return raw.lower() in ("1", "true", "yes", "on")
        
        return default

    def _normalize_print_mode(self, key: str, default: ConfigPrintMode) -> ConfigPrintMode:
        raw = self._user_config.get(key, default)

        if isinstance(raw, ConfigPrintMode):
            return raw
        
        if isinstance(raw, str):
            try:
                return ConfigPrintMode(raw.lower())
            except ValueError:
                return default
        
        return default

    @property
    def steam_url(self) -> str:
        return self._user_config.get("steam_url", "")

    @steam_url.setter
    def steam_url(self, value: str) -> None:
        if not (isinstance(value, str) or value == None):
            raise config.ConfigError("steam_url must be a string or None.")
        self._user_config["steam_url"] = value
    
    @property
    def steam_login_secure(self) -> str:
        return self._user_config.get("steamLoginSecure", "")
    
    @steam_login_secure.setter
    def steam_login_secure(self, value: str) -> None:
        if not (isinstance(value, str) or value == None):
            raise config.ConfigError("steamLoginSecure must be a string or None.")
        self._user_config["steamLoginSecure"] = value
    
    @property
    def session_id(self) -> str:
        return self._user_config.get("sessionid", "")
    
    @session_id.setter
    def session_id(self, value: str) -> None:
        if not (isinstance(value, str) or value == None):
            raise config.ConfigError("sessionid must be a string or None.")
        self._user_config["sessionid"] = value
    
    @property
    def max_pagination_depth(self) -> int:
        return self._user_config.get("MAX_PAGINATION_DEPTH", 100)

    @max_pagination_depth.setter
    def max_pagination_depth(self, value: int) -> None:
        if not isinstance(value, int):
            raise ConfigError("MAX_PAGINATION_DEPTH must be an integer.")
        
        if value <= 0:
            raise config.ConfigError("MAX_PAGINATION_DEPTH must be a positive integer.")
        
        self._user_config["MAX_PAGINATION_DEPTH"] = value
    
    @property
    def request_delay_ms(self) -> int:
        return self._user_config.get("request_delay_ms", 0)
    
    @request_delay_ms.setter
    def request_delay_ms(self, value: int) -> None:
        if not isinstance(value, int):
            raise ConfigError("request_delay_ms must be an integer.")
        
        if value < 0:
            raise config.ConfigError("request_delay_ms cannot be negative.")
        
        self._user_config["request_delay_ms"] = value
    
    @property
    def print_config_mode(self) -> ConfigPrintMode:
        return self._user_config.get("print_config_mode", ConfigPrintMode.NONE)
    
    @print_config_mode.setter
    def print_config_mode(self, value: ConfigPrintMode) -> None:
        if not isinstance(value, ConfigPrintMode):
            raise config.ConfigError("print_config_mode must be ConfigPrintMode enum")

        self._user_config["print_config_mode"] = value


    @property
    def dry_run(self) -> bool:
        return self._user_config.get("dry_run", False)
    
    @dry_run.setter
    def dry_run(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise config.ConfigError("dry_run must be a boolean.")
        self._user_config["dry_run"] = value

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