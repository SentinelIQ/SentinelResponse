from abc import ABC, abstractmethod

from sentinelresponse.logmanager.log_manager import LogManager


class Notifier(ABC):
    """Abstract interface for notification channels."""

    @abstractmethod
    def notify(self, message: str) -> None:
        """Send a notification with the specified message."""


class EmailNotifier(Notifier):
    """Notifier implementation for sending email notifications."""

    def __init__(self):
        self.logger = LogManager.get_logger()

    def notify(self, message: str) -> None:
        """Send an email notification (simulated via logging)."""
        self.logger.info(f"[Email] Sending email notification: {message}")


class SlackNotifier(Notifier):
    """Notifier implementation for sending Slack notifications."""

    def __init__(self):
        self.logger = LogManager.get_logger()

    def notify(self, message: str) -> None:
        """Send a Slack notification (simulated via logging)."""
        self.logger.info(f"[Slack] Sending Slack notification: {message}")


class MattermostNotifier(Notifier):
    """Notifier implementation for sending Mattermost notifications."""

    def __init__(self):
        self.logger = LogManager.get_logger()

    def notify(self, message: str) -> None:
        """Send a Mattermost notification (simulated via logging)."""
        self.logger.info(f"[Mattermost] Sending Mattermost notification: {message}")
