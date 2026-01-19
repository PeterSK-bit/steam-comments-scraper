class SteamClientError(Exception):
    pass

class MaxPaginationDepthExceeded(SteamClientError):
    pass

class SteamRequestFailed(SteamClientError):
    pass