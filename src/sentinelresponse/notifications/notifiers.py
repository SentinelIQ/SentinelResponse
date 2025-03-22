import logging
from abc import ABC, abstractmethod


class Notifier(ABC):
    """Abstract interface for notification channels.

    This abstract base class defines the interface that all concrete notification
    implementations must follow. Implementing classes should provide their own version
    of the `notify` method, which is responsible for sending a notification message
    using the specific channel (e.g., Email, Slack, Mattermost).

    Methods
    -------
    notify(message: str) -> None
        Sends a notification with the specified message.

    """

    @abstractmethod
    def notify(self, message: str) -> None:
        """Send a notification with the specified message.

        This method must be implemented by any subclass of Notifier. It should handle
        the process of sending a notification message via the respective channel.

        Parameters
        ----------
        message : str
            The message to be sent as a notification.

        Returns
        -------
        None

        Examples
        --------
        >>> class MyNotifier(Notifier):
        ...     def notify(self, message: str) -> None:
        ...         logging.info("Notification: " + message)
        >>> notifier = MyNotifier()
        >>> notifier.notify("Test message")

        """


class EmailNotifier(Notifier):
    """Concrete implementation of Notifier for sending notifications via email.

    This class provides an implementation of the `notify` method that simulates
    sending an email notification by logging the action.

    Methods
    -------
    notify(message: str) -> None
        Logs the sending of an email notification with the given message.

    """

    def notify(self, message: str) -> None:
        """Send an email notification with the specified message.

        This implementation logs the message to simulate the action of sending an email.

        Parameters
        ----------
        message : str
            The message to be sent in the email.

        Returns
        -------
        None

        Examples
        --------
        >>> email_notifier = EmailNotifier()
        >>> email_notifier.notify("Test email message")

        """
        logging.info(f"[Email] Enviando email: {message}")


class SlackNotifier(Notifier):
    """Concrete implementation of Notifier for sending notifications via Slack.

    This class provides an implementation of the `notify` method that simulates
    sending a Slack message by logging the action.

    Methods
    -------
    notify(message: str) -> None
        Logs the sending of a Slack notification with the given message.

    """

    def notify(self, message: str) -> None:
        """Send a Slack notification with the specified message.

        This implementation logs the message to simulate the action of sending a Slack message.

        Parameters
        ----------
        message : str
            The message to be sent via Slack.

        Returns
        -------
        None

        Examples
        --------
        >>> slack_notifier = SlackNotifier()
        >>> slack_notifier.notify("Test Slack message")

        """
        logging.info(f"[Slack] Enviando mensagem no Slack: {message}")


class MattermostNotifier(Notifier):
    """Concrete implementation of Notifier for sending notifications via Mattermost.

    This class provides an implementation of the `notify` method that simulates
    sending a Mattermost message by logging the action.

    Methods
    -------
    notify(message: str) -> None
        Logs the sending of a Mattermost notification with the given message.

    """

    def notify(self, message: str) -> None:
        """Send a Mattermost notification with the specified message.

        This implementation logs the message to simulate the action of sending a Mattermost message.

        Parameters
        ----------
        message : str
            The message to be sent via Mattermost.

        Returns
        -------
        None

        Examples
        --------
        >>> mattermost_notifier = MattermostNotifier()
        >>> mattermost_notifier.notify("Test Mattermost message")

        """
        logging.info(f"[Mattermost] Enviando mensagem no Mattermost: {message}")
