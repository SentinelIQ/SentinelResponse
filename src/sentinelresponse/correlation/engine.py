from collections.abc import Callable

from sentinelresponse.alerts.manager import AlertManager
from sentinelresponse.alerts.models import Alert
from sentinelresponse.cases.manager import CaseManager
from sentinelresponse.cases.models import Case
from sentinelresponse.logmanager.log_manager import LogManager


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
        self.logger = LogManager.get_logger()

    def correlate_alerts_to_cases(self) -> list[Case]:
        """Automatically correlate alerts to cases based on default rules."""
        new_cases: list[Case] = []
        all_alerts = self.alert_manager.read_all_alerts()
        existing_cases = self.case_manager.read_all_cases()
        correlated_alert_ids = {a.alert_id for c in existing_cases for a in c.alerts}

        for alert in all_alerts:
            if (
                alert.alert_id not in correlated_alert_ids
                and alert.severity.lower() == "alta"
            ):
                case_id = alert.alert_id + 1000
                new_case = Case(case_id=case_id, title=f"Investigação: {alert.message}")
                new_case.add_alert(alert)
                self.case_manager.create_case(new_case)
                new_cases.append(new_case)
                self.logger.info(
                    f"Alert {alert.alert_id} correlated to new case {case_id}"
                )
                if self.timeline_manager:
                    self.timeline_manager.create_event(
                        timestamp=__import__("datetime").datetime.now(),
                        description=f"Alert {alert.alert_id} correlated to case {case_id}",
                    )
                if self.notifications_manager:
                    self.notifications_manager.send_notification(
                        f"New case created from alert {alert.alert_id}: Case {case_id}"
                    )
        return new_cases

    def correlate_alerts_with_rule(
        self, rule: Callable[[Alert], bool], case_title_prefix: str = "Correlated Case"
    ) -> list[Case]:
        """Correlate alerts to cases using a custom correlation rule."""
        new_cases: list[Case] = []
        all_alerts = self.alert_manager.read_all_alerts()
        existing_cases = self.case_manager.read_all_cases()
        correlated_alert_ids = {a.alert_id for c in existing_cases for a in c.alerts}

        for alert in all_alerts:
            if alert.alert_id not in correlated_alert_ids and rule(alert):
                case_id = alert.alert_id + 1000
                new_case = Case(
                    case_id=case_id, title=f"{case_title_prefix}: {alert.message}"
                )
                new_case.add_alert(alert)
                self.case_manager.create_case(new_case)
                new_cases.append(new_case)
                self.logger.info(
                    f"Alert {alert.alert_id} correlated to new case {case_id} using custom rule"
                )
                if self.timeline_manager:
                    self.timeline_manager.create_event(
                        timestamp=__import__("datetime").datetime.now(),
                        description=f"Custom correlation: Alert {alert.alert_id} to case {case_id}",
                    )
                if self.notifications_manager:
                    self.notifications_manager.send_notification(
                        f"New case (custom rule) created from alert {alert.alert_id}: Case {case_id}"
                    )
        return new_cases

    def remove_correlation_for_alert(self, alert_id: int) -> None:
        """Remove the correlation of an alert from its associated case."""
        for case in self.case_manager.read_all_cases():
            for alert in case.alerts:
                if alert.alert_id == alert_id:
                    case.alerts.remove(alert)
                    self.logger.info(
                        f"Removed alert {alert_id} from case {case.case_id}"
                    )
                    if not case.alerts:
                        self.case_manager.delete_case(case.case_id)
                        self.logger.info(
                            f"Case {case.case_id} deleted as it became empty"
                        )
                    return

    def update_correlation_for_alert(self, updated_alert: Alert) -> None:
        """Update the correlation for a modified alert."""
        for case in self.case_manager.read_all_cases():
            for idx, alert in enumerate(case.alerts):
                if alert.alert_id == updated_alert.alert_id:
                    case.alerts[idx] = updated_alert
                    self.logger.info(
                        f"Updated alert {updated_alert.alert_id} in case {case.case_id}"
                    )
                    return
        self.logger.info(f"No case found for updated alert {updated_alert.alert_id}")
