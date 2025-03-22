import logging

from sentinelresponse.alerts.models import Alert


class NotFoundError(Exception):
    """Exception raised when an item is not found.

    This exception is used by AlertManager methods to signal that a specific
    alert, identified by its unique identifier, does not exist in the storage.

    Examples
    --------
    >>> raise NotFoundError("Alerta 1 não encontrado.")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    NotFoundError: Alerta 1 não encontrado.

    """


class AlertManager:
    """Manages alerts with support for CRUD (Create, Read, Update, Delete) operations.

    This class uses an internal dictionary to store Alert objects, keyed by their
    unique `alert_id`. It provides methods to add a new alert, retrieve an alert
    by ID, retrieve all alerts, update an existing alert, and delete an alert.

    Attributes
    ----------
    alerts : dict[int, Alert]
        A dictionary mapping alert IDs to Alert objects.

    Examples
    --------
    >>> from sentinelresponse.alerts.models import Alert
    >>> am = AlertManager()
    >>> am.alerts
    {}

    """

    def __init__(self):
        """Initialize the AlertManager with an empty alerts dictionary.

        The `alerts` dictionary is used to store Alert objects, where each key is
        the unique identifier of an alert.

        Examples
        --------
        >>> am = AlertManager()
        >>> am.alerts
        {}

        """
        self.alerts: dict[int, Alert] = {}

    def create_alert(self, alert: Alert) -> None:
        """Create a new alert and add it to the manager.

        This method logs the creation of an alert and stores the Alert object in
        the internal dictionary using its `alert_id` as the key.

        Parameters
        ----------
        alert : Alert
            The Alert object to be added. It should have a unique `alert_id` attribute.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(alert_id=1, message="Login suspeito detectado", severity="Alta")
        >>> am = AlertManager()
        >>> am.create_alert(alert)

        """
        logging.info(f"Criando alerta: {alert}")
        self.alerts[alert.alert_id] = alert

    def read_alert(self, alert_id: int) -> Alert:
        """Retrieve an alert by its unique identifier.

        This method searches for an Alert object in the internal dictionary using
        the provided `alert_id`. If found, it returns the Alert; otherwise, it
        raises a NotFoundError.

        Parameters
        ----------
        alert_id : int
            The unique identifier of the alert to retrieve.

        Returns
        -------
        Alert
            The Alert object corresponding to the given `alert_id`.

        Raises
        ------
        NotFoundError
            If no alert with the specified `alert_id` exists.

        Examples
        --------
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(alert_id=1, message="Login suspeito detectado", severity="Alta")
        >>> am = AlertManager()
        >>> am.create_alert(alert)
        >>> retrieved_alert = am.read_alert(1)
        >>> retrieved_alert.message
        'Login suspeito detectado'

        """
        if alert_id in self.alerts:
            return self.alerts[alert_id]
        raise NotFoundError(f"Alerta {alert_id} não encontrado.")

    def read_all_alerts(self) -> list[Alert]:
        """Retrieve all alerts stored in the manager.

        Returns
        -------
        list[Alert]
            A list of all Alert objects currently managed by the AlertManager.

        Examples
        --------
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert1 = Alert(alert_id=1, message="Login suspeito", severity="Alta")
        >>> alert2 = Alert(alert_id=2, message="Acesso inválido", severity="Baixa")
        >>> am = AlertManager()
        >>> am.create_alert(alert1)
        >>> am.create_alert(alert2)
        >>> all_alerts = am.read_all_alerts()
        >>> len(all_alerts)
        2

        """
        return list(self.alerts.values())

    def update_alert(self, alert: Alert) -> None:
        """Update an existing alert.

        This method replaces the Alert object with the same `alert_id` in the
        internal dictionary with the provided Alert object containing updated
        information. If the alert does not exist, a NotFoundError is raised.

        Parameters
        ----------
        alert : Alert
            The Alert object containing updated information. Its `alert_id` must
            already exist in the manager.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no alert with the given `alert_id` exists for update.

        Examples
        --------
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(alert_id=1, message="Mensagem inicial", severity="Alta")
        >>> am = AlertManager()
        >>> am.create_alert(alert)
        >>> alert.message = "Mensagem atualizada"
        >>> am.update_alert(alert)

        """
        if alert.alert_id in self.alerts:
            logging.info(f"Atualizando alerta: {alert}")
            self.alerts[alert.alert_id] = alert
        else:
            msg = f"Alerta {alert.alert_id} não encontrado para atualização."
            raise NotFoundError(msg)

    def delete_alert(self, alert_id: int) -> None:
        """Delete an alert from the manager by its unique identifier.

        This method removes the Alert object corresponding to the given `alert_id`
        from the internal dictionary. If the alert does not exist, it raises a
        NotFoundError.

        Parameters
        ----------
        alert_id : int
            The unique identifier of the alert to delete.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no alert with the specified `alert_id` is found.

        Examples
        --------
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(alert_id=1, message="Login suspeito", severity="Alta")
        >>> am = AlertManager()
        >>> am.create_alert(alert)
        >>> am.delete_alert(1)

        """
        if alert_id in self.alerts:
            logging.info(f"Excluindo alerta com ID: {alert_id}")
            del self.alerts[alert_id]
        else:
            raise NotFoundError(f"Alerta {alert_id} não encontrado para exclusão.")
