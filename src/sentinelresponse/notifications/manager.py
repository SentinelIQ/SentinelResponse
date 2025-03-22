import logging

from sentinelresponse.notifications.notifiers import Notifier


class NotificationsManager:
    """Manages notification channels and message delivery.

    This class is responsible for managing a collection of notifier objects, which are used to send
    notifications through various channels (such as email, Slack, etc.). It supports operations to add
    and remove notifiers, as well as broadcasting messages to all registered notifiers.

    Attributes
    ----------
    notifiers : list[Notifier]
        A list that stores instances of Notifier implementations.

    Examples
    --------
    >>> from sentinelresponse.notifications.notifiers import EmailNotifier
    >>> nm = NotificationsManager()
    >>> email_notifier = EmailNotifier()
    >>> nm.add_notifier(email_notifier)
    >>> nm.send_notification("Test message")

    """

    def __init__(self):
        """Initialize a new NotificationsManager with an empty list of notifiers.

        Examples
        --------
        >>> nm = NotificationsManager()
        >>> nm.notifiers
        []

        """
        self.notifiers: list[Notifier] = []

    def add_notifier(self, notifier: Notifier) -> None:
        """Add a notifier to the manager.

        This method registers a new notifier with the NotificationsManager. Once added, the notifier
        will receive messages when send_notification is invoked.

        Parameters
        ----------
        notifier : Notifier
            An instance of a class that implements the Notifier interface.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.notifications.notifiers import EmailNotifier
        >>> nm = NotificationsManager()
        >>> email_notifier = EmailNotifier()
        >>> nm.add_notifier(email_notifier)

        """
        logging.info(f"Adicionando notifier: {notifier.__class__.__name__}")
        self.notifiers.append(notifier)

    def remove_notifier(self, notifier: Notifier) -> None:
        """Remove a notifier from the manager.

        This method unregisters the specified notifier from the NotificationsManager. If the notifier
        is not found in the list, a warning message is logged.

        Parameters
        ----------
        notifier : Notifier
            The notifier instance to remove.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.notifications.notifiers import EmailNotifier
        >>> nm = NotificationsManager()
        >>> email_notifier = EmailNotifier()
        >>> nm.add_notifier(email_notifier)
        >>> nm.remove_notifier(email_notifier)

        """
        if notifier in self.notifiers:
            logging.info(f"Removendo notifier: {notifier.__class__.__name__}")
            self.notifiers.remove(notifier)
        else:
            logging.warning("Notifier não encontrado para remoção.")

    def send_notification(self, message: str) -> None:
        """Send a notification message to all registered notifiers.

        This method iterates over each registered notifier and calls its notify method,
        passing the provided message. It enables the broadcasting of a single message across
        multiple notification channels.

        Parameters
        ----------
        message : str
            The message to send to all registered notifiers.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.notifications.notifiers import EmailNotifier
        >>> nm = NotificationsManager()
        >>> email_notifier = EmailNotifier()
        >>> nm.add_notifier(email_notifier)
        >>> nm.send_notification("Test message")

        """
        for notifier in self.notifiers:
            notifier.notify(message)
