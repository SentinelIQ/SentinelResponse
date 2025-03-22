from sentinelresponse.cases.models import Case
from sentinelresponse.logmanager.log_manager import LogManager


class CaseReporter:
    """Responsible for generating reports for security cases.

    This class provides methods for generating case reports in different formats.
    Currently, it supports generating reports in Markdown and a simulation of PDF report
    generation. These reports detail the case information, including the title, case ID,
    and associated alerts.
    """

    def __init__(self):
        self.logger = LogManager.get_logger()

    def generate_report_markdown(self, case: Case) -> str:
        """Generates a Markdown formatted report for the specified case."""
        report = f"# Case Report: {case.title}\n"
        report += f"Case ID: {case.case_id}\n"
        report += "## Alerts:\n"
        for alert in case.alerts:
            report += (
                f"- ID {alert.alert_id}: {alert.message} (Severity: {alert.severity})\n"
            )

        self.logger.info("Markdown report generated successfully.")
        return report.rstrip()

    def generate_report_pdf(self, case: Case) -> str:
        """Simulates the generation of a PDF report for the specified case."""
        self.logger.info(f"Generating PDF report for case {case.case_id}")
        # Placeholder for real PDF generation integration
        return f"PDF report for case {case.case_id}"
