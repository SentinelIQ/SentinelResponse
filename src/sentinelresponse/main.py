from datetime import datetime

from sentinelresponse.alerts.manager import AlertManager
from sentinelresponse.alerts.models import Alert
from sentinelresponse.apis.api import API
from sentinelresponse.cases.manager import CaseManager
from sentinelresponse.cases.models import Case
from sentinelresponse.correlation.engine import CorrelationEngine
from sentinelresponse.integrations.misp import MISPIntegration
from sentinelresponse.integrations.mitre import MitreIntegration
from sentinelresponse.knowledgebase.manager import KnowledgeBase
from sentinelresponse.logmanager.log_manager import LogManager
from sentinelresponse.metrics.manager import MetricsManager
from sentinelresponse.notifications.manager import NotificationsManager
from sentinelresponse.notifications.notifiers import EmailNotifier, SlackNotifier
from sentinelresponse.reporting.case_reporter import CaseReporter
from sentinelresponse.tenants.manager import TenantManager
from sentinelresponse.tenants.models import Tenant
from sentinelresponse.timeline.manager import TimelineManager
from sentinelresponse.users.manager import UserManager
from sentinelresponse.users.models import User

logger = LogManager.get_logger()


def main() -> None:
    """Demonstrates a complete usage example of the Security Incident Response System."""
    (
        alert_manager,
        case_manager,
        user_manager,
        tenant_manager,
        notifications_manager,
        metrics_manager,
        timeline_manager,
        knowledge_base,
        correlation_engine,
        misp_integration,
        mitre_integration,
        case_reporter,
        api,
    ) = initialize_components()

    create_sample_alerts(alert_manager)
    manual_case = create_manual_case(alert_manager, case_manager)
    create_user_and_tenant(user_manager, tenant_manager)
    setup_notifications(notifications_manager)
    update_metrics(metrics_manager, alert_manager, case_manager)
    log_timeline_event(timeline_manager)
    correlate_alerts(correlation_engine)
    import_threat_intel(misp_integration, mitre_integration)
    generate_reports(case_reporter, manual_case)
    manage_knowledge_base(knowledge_base, manual_case)
    output_api_data(api)
    output_timeline_events(timeline_manager)


def initialize_components():
    alert_manager = AlertManager()
    case_manager = CaseManager()
    user_manager = UserManager()
    tenant_manager = TenantManager()
    notifications_manager = NotificationsManager()
    metrics_manager = MetricsManager()
    timeline_manager = TimelineManager()
    knowledge_base = KnowledgeBase()

    correlation_engine = CorrelationEngine(
        alert_manager, case_manager, timeline_manager, notifications_manager
    )
    misp_integration = MISPIntegration()
    mitre_integration = MitreIntegration()
    case_reporter = CaseReporter()

    api = API(alert_manager, case_manager, user_manager)

    return (
        alert_manager,
        case_manager,
        user_manager,
        tenant_manager,
        notifications_manager,
        metrics_manager,
        timeline_manager,
        knowledge_base,
        correlation_engine,
        misp_integration,
        mitre_integration,
        case_reporter,
        api,
    )


def create_sample_alerts(alert_manager):
    for idx, (msg, sev) in enumerate(
        [
            ("Suspicious login detected", "High"),
            ("Out-of-hours access detected", "Medium"),
            ("Invalid login attempt", "Low"),
        ],
        start=1,
    ):
        alert = Alert(alert_id=idx, message=msg, severity=sev)
        alert_manager.create_alert(alert)


def create_manual_case(alert_manager, case_manager):
    manual_case = Case(case_id=101, title="Manual Investigation: Suspicious Login")
    manual_case.add_alert(alert_manager.read_alert(1))
    case_manager.create_case(manual_case)
    return manual_case


def create_user_and_tenant(user_manager, tenant_manager):
    user = User(user_id=1001, username="analyst1", email="analyst1@example.com")
    user_manager.create_user(user)
    tenant = Tenant(tenant_id=201, name="Finance")
    tenant_manager.create_tenant(tenant)


def setup_notifications(notifications_manager):
    notifications_manager.add_notifier(EmailNotifier())
    notifications_manager.add_notifier(SlackNotifier())
    notifications_manager.send_notification(
        "New case registered: Manual Suspicious Login Investigation"
    )


def update_metrics(metrics_manager, alert_manager, case_manager):
    metrics_manager.set_metric(
        "total_alerts", float(len(alert_manager.read_all_alerts()))
    )
    metrics_manager.set_metric("total_cases", float(len(case_manager.read_all_cases())))
    logger.info("\n" + metrics_manager.generate_dashboard())


def log_timeline_event(timeline_manager):
    timeline_manager.create_event(
        datetime.now(tz=datetime.timezone.utc), "System started and data loaded."
    )


def correlate_alerts(correlation_engine):
    new_cases = correlation_engine.correlate_alerts_to_cases()
    if new_cases:
        for nc in new_cases:
            logger.info(f"Auto-generated case: {nc}")
    else:
        logger.info("No new cases generated by correlation.")


def import_threat_intel(misp_integration, mitre_integration):
    misp_integration.import_iocs()
    mitre_integration.import_tactics()


def generate_reports(case_reporter, manual_case):
    md_report = case_reporter.generate_report_markdown(manual_case)
    logger.info("\nMarkdown Report:\n" + md_report)
    pdf_report = case_reporter.generate_report_pdf(manual_case)
    logger.info("\nPDF Report:\n" + pdf_report)


def manage_knowledge_base(knowledge_base, manual_case):
    knowledge_base.create_article(
        title="Security Policy",
        content="All incidents must be reported within 24 hours.",
        linked_cases=[manual_case.case_id],
        linked_alerts=[1],
    )
    article = knowledge_base.read_article("Security Policy")
    logger.info(f"Knowledge Base article loaded: {article}")


def output_api_data(api):
    logger.info("API — Alerts:")
    for a in api.get_alerts():
        logger.info(a)
    logger.info("API — Cases:")
    for c in api.get_cases():
        logger.info(c)
    logger.info("API — Users:")
    for u in api.get_users():
        logger.info(u)


def output_timeline_events(timeline_manager):
    logger.info("Timeline Events:")
    for timestamp, desc in timeline_manager.read_events():
        logger.info(f"{timestamp} — {desc}")


if __name__ == "__main__":
    main()
