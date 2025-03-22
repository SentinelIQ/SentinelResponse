import logging
from datetime import datetime

# Import managers and models from the system
from sentinelresponse.alerts.manager import AlertManager
from sentinelresponse.alerts.models import Alert
from sentinelresponse.apis.api import API
from sentinelresponse.cases.manager import CaseManager
from sentinelresponse.cases.models import Case
from sentinelresponse.correlation.engine import CorrelationEngine
from sentinelresponse.integrations.misp import MISPIntegration
from sentinelresponse.integrations.mitre import MitreIntegration
from sentinelresponse.knowledgebase.manager import KnowledgeBase
from sentinelresponse.metrics.manager import MetricsManager
from sentinelresponse.notifications.manager import NotificationsManager
from sentinelresponse.notifications.notifiers import (
    EmailNotifier,
    SlackNotifier,
)
from sentinelresponse.reporting.case_reporter import CaseReporter
from sentinelresponse.tenants.manager import TenantManager
from sentinelresponse.tenants.models import Tenant
from sentinelresponse.timeline.manager import TimelineManager
from sentinelresponse.users.manager import UserManager
from sentinelresponse.users.models import User

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)


def main() -> None:  # noqa: PLR0915
    """Demonstrates a complete usage example of the Security Incident Response System.

    This example initializes various managers for alerts, cases, users, tenants,
    notifications, metrics, timeline, and integrations. It then creates sample data
    (alerts, cases, users, tenants), performs CRUD operations, correlates alerts with
    cases, sends notifications, updates metrics, logs timeline events, generates reports,
    and exposes the data via a simple API interface.

    Examples
    --------
    >>> if __name__ == "__main__":
    ...     main()

    """
    # Initialize managers
    alert_manager = AlertManager()
    case_manager = CaseManager()
    user_manager = UserManager()
    tenant_manager = TenantManager()
    notifications_manager = NotificationsManager()
    metrics_manager = MetricsManager()
    timeline_manager = TimelineManager()
    knowledge_base = KnowledgeBase()

    # Initialize integrations and reporting
    correlation_engine = CorrelationEngine(
        alert_manager, case_manager, timeline_manager, notifications_manager
    )
    misp_integration = MISPIntegration()
    mitre_integration = MitreIntegration()
    case_reporter = CaseReporter()

    # Initialize API facade
    api = API(alert_manager, case_manager, user_manager)

    # Create sample alerts
    alert1 = Alert(alert_id=1, message="Login suspeito detectado", severity="Alta")
    alert2 = Alert(
        alert_id=2, message="Acesso fora do horário detectado", severity="Média"
    )
    alert3 = Alert(alert_id=3, message="Tentativa de acesso inválido", severity="Baixa")

    alert_manager.create_alert(alert1)
    alert_manager.create_alert(alert2)
    alert_manager.create_alert(alert3)

    # Create a case manually and associate an alert
    case_manual = Case(case_id=101, title="Investigação Manual: Login Suspeito")
    case_manual.add_alert(alert1)
    case_manager.create_case(case_manual)

    # Create a user and tenant
    user = User(user_id=1001, username="analyst1", email="analyst1@example.com")
    user_manager.create_user(user)
    tenant = Tenant(tenant_id=201, name="Financeiro")
    tenant_manager.create_tenant(tenant)

    # Setup notifications
    notifications_manager.add_notifier(EmailNotifier())
    notifications_manager.add_notifier(SlackNotifier())
    notifications_manager.send_notification(
        "Novo caso registrado: Investigação Manual de Login Suspeito"
    )

    # Update metrics
    metrics_manager.set_metric(
        "total_alertas", float(len(alert_manager.read_all_alerts()))
    )
    metrics_manager.set_metric("total_casos", float(len(case_manager.read_all_cases())))
    logging.info("\n" + metrics_manager.generate_dashboard())

    # Add a timeline event
    timeline_manager.create_event(
        datetime.now(), "Sistema iniciado e dados carregados."
    )

    # Use the correlation engine to automatically correlate alerts of high severity
    # (alert1 is already in a manual case; alert2 and alert3 are processed based on their severity)
    new_cases = correlation_engine.correlate_alerts_to_cases()
    if new_cases:
        for new_case in new_cases:
            logging.info(f"Novo caso gerado automaticamente: {new_case}")
    else:
        logging.info("Nenhum novo caso gerado pela correlação.")

    # Import threat intelligence via integrations
    misp_integration.import_iocs()
    mitre_integration.import_tactics()

    # Generate a report for a case
    markdown_report = case_reporter.generate_report_markdown(case_manual)
    logging.info("\nRelatório Markdown:\n" + markdown_report)
    pdf_report = case_reporter.generate_report_pdf(case_manual)
    logging.info("\nRelatório PDF:\n" + pdf_report)

    # Add an article to the knowledge base and link it to the manual case and alert1
    knowledge_base.create_article(
        title="Política de Segurança",
        content="Todos os incidentes devem ser reportados em até 24 horas.",
        linked_cases=[case_manual.case_id],
        linked_alerts=[alert1.alert_id],
    )
    article = knowledge_base.read_article("Política de Segurança")
    logging.info(f"Artigo na Knowledge Base: {article}")

    # Use the API to fetch data
    all_alerts = api.get_alerts()
    all_cases = api.get_cases()
    all_users = api.get_users()
    logging.info("\nAPI - Alertas:")
    for alert in all_alerts:
        logging.info(alert)
    logging.info("\nAPI - Casos:")
    for case in all_cases:
        logging.info(case)
    logging.info("\nAPI - Usuários:")
    for user in all_users:
        logging.info(user)

    # Read and display timeline events
    timeline_events = timeline_manager.read_events()
    logging.info("\nTimeline de Eventos:")
    for event in timeline_events:
        logging.info(f"{event[0]} - {event[1]}")


if __name__ == "__main__":
    main()
