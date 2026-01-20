import logging

class DryRunManager:
    def __init__(self, logger: logging.Logger,dry_run: bool = False):
        self.dry_run_mode = dry_run
        self.logger = logger

    def execute(self, description: str, func: callable, *args, **kwargs):
        """
        Executes the function if dry_run is False, else logs the action.

        :param description: str - human-readable description of what would happen
        :param func: callable - function to execute
        """
        if self.dry_run_mode:
            self.logger.dry_run(f"Would execute: {description}")
            return None
        else:
            self.logger.dry_run(f"Executing: {description}")
            return func(*args, **kwargs)
    
    @property
    def is_dry_run(self) -> bool:
        return self.dry_run_mode