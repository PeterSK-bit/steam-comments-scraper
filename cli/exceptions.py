class CLIException(Exception):
    pass

class InvalidCLIArgument(CLIException):
    pass

class MissingCLIArgument(CLIException):
    pass

class CLIArgumentConflict(CLIException):
    pass