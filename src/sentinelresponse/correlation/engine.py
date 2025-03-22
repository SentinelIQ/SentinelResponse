import logging
from collections.abc import Callable

from sentinelresponse.alerts.manager import AlertManager
from sentinelresponse.alerts.models import Alert
from sentinelresponse.cases.manager import CaseManager
from sentinelresponse.cases.models import Case


class CorrelationEngine:
    """Engine for correlating alerts with cases and managing complex correlation operations.

    This engine integrates with the entire system by automatically correlating alerts
    with cases based on defined rules, as well as supporting advanced operations such as
    custom rule-based correlation, updating correlations, and removing correlations. It
    can also integrate with additional system modules (such as timeline and notifications)
    to provide a comprehensive incident response workflow.

    Parameters
    ----------
    alert_manager : AlertManager
        Manager responsible for handling alerts.
    case_manager : CaseManager
        Manager responsible for handling cases.
    timeline_manager : optional
        Manager for timeline events. If provided, timeline events will be created upon correlation.
    notifications_manager : optional
        Manager for sending notifications. If provided, notifications will be sent upon correlation events.

    Attributes
    ----------
    alert_manager : AlertManager
        Instance managing alerts.
    case_manager : CaseManager
        Instance managing cases.
    timeline_manager : optional
        Instance managing timeline events.
    notifications_manager : optional
        Instance managing notifications.

    Examples
    --------
    >>> from sentinelresponse.alerts.manager import AlertManager
    >>> from sentinelresponse.cases.manager import CaseManager
    >>> from sentinelresponse.alerts.models import Alert
    >>> ce = CorrelationEngine(AlertManager(), CaseManager())
    >>> alert = Alert(alert_id=1, message="Test alert", severity="alta")
    >>> ce.alert_manager.create_alert(alert)
    >>> new_cases = ce.correlate_alerts_to_cases()
    >>> print(new_cases[0].title)
    Investigação: Test alert

    """

    def __init__(
        self,
        alert_manager: AlertManager,
        case_manager: CaseManager,
        timeline_manager: object | None = None,
        notifications_manager: object | None = None,
    ):
        self.alert_manager = alert_manager
        self.case_manager = case_manager
        self.timeline_manager = timeline_manager
        self.notifications_manager = notifications_manager

    def correlate_alerts_to_cases(self) -> list[Case]:
        """Automatically correlate alerts to cases based on default rules.

        This method scans all alerts and identifies those that have not yet been
        correlated with any case. It applies a default rule: if an alert's severity is
        "alta" (high), a new case is created for that alert. Newly created cases are
        registered with the case manager, and if timeline or notifications managers are
        provided, corresponding events and notifications are triggered.

        Returns
        -------
        list[Case]
            A list of new Case objects generated through the correlation process.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> ce = CorrelationEngine(AlertManager(), CaseManager())
        >>> alert = Alert(alert_id=1, message="Test alert", severity="alta")
        >>> ce.alert_manager.create_alert(alert)
        >>> new_cases = ce.correlate_alerts_to_cases()
        >>> print(new_cases[0].title)
        Investigação: Test alert

        """
        new_cases: list[Case] = []
        all_alerts = self.alert_manager.read_all_alerts()
        existing_cases = self.case_manager.read_all_cases()

        # Gather IDs of alerts already correlated in any case
        correlated_alert_ids = {
            alert.alert_id for case in existing_cases for alert in case.alerts
        }

        for alert in all_alerts:
            # Default correlation rule: if not correlated and severity is "alta", create a new case.
            if (
                alert.alert_id not in correlated_alert_ids
                and alert.severity.lower() == "alta"
            ):
                case_id = alert.alert_id + 1000  # Simple case ID generation.
                new_case = Case(case_id=case_id, title=f"Investigação: {alert.message}")
                new_case.add_alert(alert)
                self.case_manager.create_case(new_case)
                new_cases.append(new_case)
                logging.info(f"Alert {alert.alert_id} correlated to new case {case_id}")
                if self.timeline_manager is not None:
                    self.timeline_manager.create_event(
                        timestamp=__import__("datetime").datetime.now(),
                        description=f"Alert {alert.alert_id} correlated to case {case_id}",
                    )
                if self.notifications_manager is not None:
                    self.notifications_manager.send_notification(
                        f"New case created from alert {alert.alert_id}: Case {case_id}"
                    )
        return new_cases

    def correlate_alerts_with_rule(
        self, rule: Callable[[Alert], bool], case_title_prefix: str = "Correlated Case"
    ) -> list[Case]:
        """Correlate alerts to cases using a custom correlation rule.

        This method applies a user-provided rule—a callable that accepts an Alert and
        returns a boolean—to determine whether an alert should be correlated into a new case.
        For each alert satisfying the rule and not already correlated, a new case is created
        with a title prefixed by `case_title_prefix`.

        Parameters
        ----------
        rule : Callable[[Alert], bool]
            A function that takes an Alert object as input and returns True if the alert
            should be correlated.
        case_title_prefix : str, optional
            A prefix for the title of the generated case. Default is "Correlated Case".

        Returns
        -------
        list[Case]
            A list of new Case objects created based on the custom correlation rule.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> def custom_rule(alert):
        ...     return "suspicious" in alert.message.lower()
        >>> ce = CorrelationEngine(AlertManager(), CaseManager())
        >>> alert = Alert(alert_id=2, message="Suspicious activity detected", severity="low")
        >>> ce.alert_manager.create_alert(alert)
        >>> new_cases = ce.correlate_alerts_with_rule(custom_rule, "Suspicious Alert")
        >>> print(new_cases[0].title)
        Suspicious Alert: Suspicious activity detected

        """
        new_cases: list[Case] = []
        all_alerts = self.alert_manager.read_all_alerts()
        existing_cases = self.case_manager.read_all_cases()
        correlated_alert_ids = {
            alert.alert_id for case in existing_cases for alert in case.alerts
        }

        for alert in all_alerts:
            if alert.alert_id not in correlated_alert_ids and rule(alert):
                case_id = alert.alert_id + 1000
                new_case = Case(
                    case_id=case_id, title=f"{case_title_prefix}: {alert.message}"
                )
                new_case.add_alert(alert)
                self.case_manager.create_case(new_case)
                new_cases.append(new_case)
                logging.info(
                    f"Alert {alert.alert_id} correlated to new case {case_id} using custom rule"
                )
                if self.timeline_manager is not None:
                    self.timeline_manager.create_event(
                        timestamp=__import__("datetime").datetime.now(),
                        description=f"Custom correlation: Alert {alert.alert_id} to case {case_id}",
                    )
                if self.notifications_manager is not None:
                    self.notifications_manager.send_notification(
                        f"New case (custom rule) created from alert {alert.alert_id}: Case {case_id}"
                    )
        return new_cases

    def remove_correlation_for_alert(self, alert_id: int) -> None:
        """Remove the correlation of an alert from its associated case.

        This method searches through all cases to locate an alert with the specified
        alert_id and removes it from the corresponding case's list of alerts. If the
        removal leaves the case with no alerts, the case is deleted from the case manager.

        Parameters
        ----------
        alert_id : int
            The unique identifier of the alert whose correlation is to be removed.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> ce = CorrelationEngine(AlertManager(), CaseManager())
        >>> alert = Alert(alert_id=3, message="Test alert", severity="alta")
        >>> ce.alert_manager.create_alert(alert)
        >>> _ = ce.correlate_alerts_to_cases()  # Suppress output
        >>> ce.remove_correlation_for_alert(3)

        """
        cases = self.case_manager.read_all_cases()
        for case in cases:
            for alert in case.alerts:
                if alert.alert_id == alert_id:
                    case.alerts.remove(alert)
                    logging.info(f"Removed alert {alert_id} from case {case.case_id}")
                    if not case.alerts:
                        self.case_manager.delete_case(case.case_id)
                        logging.info(f"Case {case.case_id} deleted as it became empty")
                    return

    def update_correlation_for_alert(self, updated_alert: Alert) -> None:
        """Update the correlation for a modified alert.

        This method locates the case containing the alert with the same alert_id as the
        updated_alert, then replaces the old alert with the updated one. If the alert is
        not found in any case, no action is taken.

        Parameters
        ----------
        updated_alert : Alert
            The updated Alert object that should replace the existing alert in its correlated case.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> ce = CorrelationEngine(AlertManager(), CaseManager())
        >>> alert = Alert(alert_id=4, message="Old message", severity="alta")
        >>> ce.alert_manager.create_alert(alert)
        >>> _ = ce.correlate_alerts_to_cases()  # Suppress output
        >>> updated_alert = Alert(alert_id=4, message="Updated message", severity="alta")
        >>> ce.update_correlation_for_alert(updated_alert)

        """
        cases = self.case_manager.read_all_cases()
        for case in cases:
            for i, alert in enumerate(case.alerts):
                if alert.alert_id == updated_alert.alert_id:
                    case.alerts[i] = updated_alert
                    logging.info(
                        f"Updated alert {updated_alert.alert_id} in case {case.case_id}"
                    )
                    return
        logging.info(f"No case found for updated alert {updated_alert.alert_id}")
