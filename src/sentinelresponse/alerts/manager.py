"""This module provides the AlertManager class for managing Alert objects with CRUD operations,
and the NotFoundError exception for handling missing alerts.
"""

from sentinelresponse.alerts.models import Alert
from sentinelresponse.logmanager.log_manager import LogManager


class NotFoundError(Exception):
    """Exception raised when an item is not found in the AlertManager's internal storage.

    Attributes
    ----------
        message (str): Detailed description of the error.

    """

    def __init__(self, message: str) -> None:
        """Initialize the NotFoundError with a detailed error message.

        Parameters
        ----------
        message : str
            Detailed description of the error.

        """
        super().__init__(message)
        self.message = message


class AlertManager:
    """A manager class providing Create, Read, Update, and Delete (CRUD) operations for Alert objects,
    with each operation being logged via the LogManager.

    Attributes
    ----------
        alerts (dict[int, Alert]): In-memory storage mapping alert IDs to Alert instances.
        logger (logging.Logger): Logger instance obtained from LogManager for recording operation details.

    """

    def __init__(self) -> None:
        """Initialize an AlertManager with empty storage and a configured logger."""
        self.alerts: dict[int, Alert] = {}
        self.logger = LogManager.get_logger()

    def create_alert(self, alert: Alert) -> None:
        """Create a new alert and store it in the manager.

        If an alert with the same alert_id already exists, a warning is logged and the
        alert is not added again.

        Parameters
        ----------
        alert : Alert
            The Alert instance to store.

        Returns
        -------
        None

        Example
        -------
        >>> manager = AlertManager()
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(1, "Test message", "LOW")
        >>> manager.create_alert(alert)
        >>> manager.read_alert(1).alert_id
        1
        >>> # Creating the same alert again does nothing (no exception)
        >>> manager.create_alert(alert)

        """
        if alert.alert_id in self.alerts:
            self.logger.warning("Attempt to create an existing alert: %s", alert)
            return

        self.alerts[alert.alert_id] = alert
        self.logger.info("Alert created: %s", alert)

    def read_alert(self, alert_id: int) -> Alert:
        """Retrieve an alert by its alert_id.

        This method fetches the alert from the internal dictionary. If the alert is not
        found, an error is logged and a NotFoundError is raised.

        Parameters
        ----------
        alert_id : int
            The unique identifier of the alert to retrieve.

        Returns
        -------
        Alert
            The Alert instance corresponding to the provided ID.

        Raises
        ------
        NotFoundError
            If no Alert with the given ID exists.

        Example
        -------
        >>> manager = AlertManager()
        >>> alert = Alert(2, "Test read", "MEDIUM")
        >>> manager.create_alert(alert)
        >>> manager.read_alert(2).alert_id
        2
        >>> # Retrieving a non-existent alert raises the fully-qualified exception
        >>> manager.read_alert(999)  # nonexistent ID
        Traceback (most recent call last):
        ...
        sentinelresponse.alerts.manager.NotFoundError: Alert 999 not found.

        """
        try:
            alert = self.alerts[alert_id]
            self.logger.debug("Alert retrieved: %s", alert)
            return alert
        except KeyError:
            msg = f"Alert {alert_id} not found."
            self.logger.error(msg)
            raise NotFoundError(msg)

    def read_all_alerts(self) -> list[Alert]:
        """Retrieve all stored Alerts.

        Returns
        -------
            list[Alert]: A list of all Alert instances currently stored.

        >>> manager = AlertManager()
        >>> manager.read_all_alerts()
        []

        """
        alerts = list(self.alerts.values())
        self.logger.debug("Retrieved all alerts (count=%d)", len(alerts))
        return alerts

    def update_alert(self, alert: Alert) -> None:
        """Update an existing alert with new information.

        The alert must already exist in the internal dictionary; otherwise, a NotFoundError
        is raised. If the alert exists, it is replaced by the new alert object.

        Parameters
        ----------
        alert : Alert
            The Alert instance with updated data. Its ID must exist in storage.

        Raises
        ------
        NotFoundError
            If attempting to update an Alert that does not exist.

        Example
        -------
        >>> manager = AlertManager()
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(2, "Initial message", "LOW")
        >>> manager.create_alert(alert)
        >>> updated = Alert(2, "Updated message", "HIGH")
        >>> manager.update_alert(updated)
        >>> manager.read_alert(2).alert_id
        2
        >>> # Attempting to update a non-existent alert raises the fully-qualified exception
        >>> manager.update_alert(Alert(999, "Nope", "LOW"))
        Traceback (most recent call last):
        ...
        sentinelresponse.alerts.manager.NotFoundError: Alert 999 not found for update.

        """
        if alert.alert_id not in self.alerts:
            msg = f"Alert {alert.alert_id} not found for update."
            self.logger.error(msg)
            raise NotFoundError(msg)

        self.alerts[alert.alert_id] = alert
        self.logger.info("Alert updated: %s", alert)

    def delete_alert(self, alert_id: int) -> None:
        """Delete an alert from the manager using its alert_id.

        If the alert is not found, an error is logged and a NotFoundError is raised.

        Parameters
        ----------
        alert_id : int
            Unique identifier of the Alert to delete.

        Raises
        ------
        NotFoundError
            If attempting to delete an Alert that does not exist.

        Example
        -------
        >>> manager = AlertManager()
        >>> alert = Alert(4, "Test delete", "LOW")
        >>> manager.create_alert(alert)
        >>> manager.delete_alert(4)
        >>> # Attempting to delete a nonexistent alert raises the fullyqualified exception
        >>> manager.delete_alert(123)  # nonexistent deletion
        Traceback (most recent call last):
        ...
        sentinelresponse.alerts.manager.NotFoundError: Alert 123 not found for deletion.

        """
        if alert_id not in self.alerts:
            msg = f"Alert {alert_id} not found for deletion."
            self.logger.error(msg)
            raise NotFoundError(msg)

        del self.alerts[alert_id]
        self.logger.info("Alert deleted (ID=%d)", alert_id)
