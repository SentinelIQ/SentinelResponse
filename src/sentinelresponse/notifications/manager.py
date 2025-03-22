from sentinelresponse.logmanager.log_manager import LogManager
from sentinelresponse.notifications.notifiers import Notifier


class NotificationsManager:
    """Manages notification channels and message delivery.

    This class is responsible for registering multiple notifier implementations
    (e.g., email, Slack) and broadcasting messages to all registered channels.

    Attributes
    ----------
    notifiers : list[Notifier]
        A list of notifier instances.
    """

    def __init__(self):
        """Initialize a new NotificationsManager with no notifiers."""
        self.notifiers: list[Notifier] = []
        self.logger = LogManager.get_logger()

    def add_notifier(self, notifier: Notifier) -> None:
        """Register a notifier to receive broadcasted messages."""
        self.logger.info(f"Adding notifier: {notifier.__class__.__name__}")
        self.notifiers.append(notifier)

    def remove_notifier(self, notifier: Notifier) -> None:
        """Unregister a notifier from receiving messages."""
        if notifier in self.notifiers:
            self.logger.info(f"Removing notifier: {notifier.__class__.__name__}")
            self.notifiers.remove(notifier)
        else:
            self.logger.warning(
                f"Notifier {notifier.__class__.__name__} not found for removal."
            )

    def send_notification(self, message: str) -> None:
        """Broadcast a message to all registered notifiers."""
        self.logger.info(f"Sending notification to {len(self.notifiers)} channels")
        for notifier in self.notifiers:
            try:
                notifier.notify(message)
                self.logger.debug(
                    f"Notification sent via {notifier.__class__.__name__}"
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to send notification via {notifier.__class__.__name__}: {e}",
                    exc_info=True,
                )
