from sentinelresponse.alerts.models import Alert


class Case:
    """Represents a security case that can contain one or more alerts.

    This class encapsulates a security case, which is used to aggregate and
    manage one or more security alerts. Each case is uniquely identified by its
    case_id and has an associated title. Alerts can be added to a case using
    the provided methods.

    Parameters
    ----------
    case_id : int
        Unique identifier for the case.
    title : str
        Title or description of the case.
    alerts : list[Alert] or None, optional
        A list of Alert objects associated with the case. If None, an empty
        list is initialized by default.

    Attributes
    ----------
    case_id : int
        Unique identifier for the case.
    title : str
        Title or description of the case.
    alerts : list[Alert]
        List of alerts that are associated with the case.

    Examples
    --------
    >>> from sentinelresponse.alerts.models import Alert
    >>> case = Case(case_id=101, title="Investigation Case")
    >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
    >>> case.add_alert(alert)
    >>> print(case)
    Case(id=101, title='Investigation Case')

    """

    def __init__(self, case_id: int, title: str, alerts: list[Alert] | None = None):
        """Initialize a new Case.

        Parameters
        ----------
        case_id : int
            Unique identifier for the case.
        title : str
            Title or description of the case.
        alerts : list[Alert] or None, optional
            A list of Alert objects to initialize the case with. Defaults to None,
            in which case an empty list is created.

        """
        self.case_id = case_id
        self.title = title
        self.alerts = alerts if alerts is not None else []

    def add_alert(self, alert: Alert) -> None:
        """Add an alert to the case.

        This method adds the given Alert object to the case's list of alerts,
        if it is not already present.

        Parameters
        ----------
        alert : Alert
            The Alert object to add to the case.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.models import Alert
        >>> case = Case(case_id=101, title="Investigation Case")
        >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
        >>> case.add_alert(alert)

        """
        if alert not in self.alerts:
            self.alerts.append(alert)

    def __repr__(self) -> str:
        """Return the official string representation of the Case.

        Returns
        -------
        str
            A string representation of the Case, including its id and title.

        Examples
        --------
        >>> case = Case(case_id=101, title="Investigation Case")
        >>> repr(case)
        "Case(id=101, title='Investigation Case')"

        """
        return f"Case(id={self.case_id}, title='{self.title}')"
