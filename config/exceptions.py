class ConfigError(Exception):
    pass

class EnvFileNotFound(ConfigError):
    pass

class EnvLoadError(ConfigError):
    pass

class EnvFilePathNotProvided(ConfigError):
    pass