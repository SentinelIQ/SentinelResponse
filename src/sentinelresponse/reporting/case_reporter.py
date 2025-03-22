import logging

from sentinelresponse.cases.models import Case


class CaseReporter:
    """Responsible for generating reports for security cases.

    This class provides methods for generating case reports in different formats.
    Currently, it supports generating reports in Markdown and a simulation of PDF report
    generation. These reports detail the case information, including the title, case ID,
    and associated alerts.

    Attributes
    ----------
    None

    Examples
    --------
    >>> from sentinelresponse.cases.models import Case
    >>> from sentinelresponse.alerts.models import Alert
    >>> # Create a case and add an alert
    >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
    >>> case = Case(case_id=101, title="Incident Investigation")
    >>> case.add_alert(alert)
    >>> reporter = CaseReporter()
    >>> print(reporter.generate_report_markdown(case))
    # Case Report: Incident Investigation
    Case ID: 101
    ## Alerts:
    - ID 1: Suspicious login detected (Severity: High)
    >>> print(reporter.generate_report_pdf(case))
    PDF report for case 101

    """

    def generate_report_markdown(self, case: Case) -> str:
        """Generates a Markdown formatted report for the specified case.

        This method generates a detailed Markdown report containing the case title,
        case ID, and the list of associated alerts, including each alert's ID, message,
        and severity.

        Parameters
        ----------
        case : Case
            Case object for which the report will be generated. The object should contain an ID,
            title, and a list of associated alerts.

        Returns
        -------
        str
            A string containing the report formatted in Markdown.

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
        >>> case = Case(case_id=101, title="Incident Investigation")
        >>> case.add_alert(alert)
        >>> reporter = CaseReporter()
        >>> markdown_report = reporter.generate_report_markdown(case)
        >>> print(markdown_report)
        # Case Report: Incident Investigation
        Case ID: 101
        ## Alerts:
        - ID 1: Suspicious login detected (Severity: High)

        """
        report = f"# Case Report: {case.title}\n"
        report += f"Case ID: {case.case_id}\n"
        report += "## Alerts:\n"
        for alert in case.alerts:
            report += (
                f"- ID {alert.alert_id}: {alert.message} (Severity: {alert.severity})\n"
            )
        logging.info("Markdown report generated successfully.")
        return report.rstrip()

    def generate_report_pdf(self, case: Case) -> str:
        """Simulates the generation of a PDF report for the specified case.

        This method simulates the creation of a PDF report for the case, returning a
        message indicating that the PDF was generated. In a real implementation, this method
        would integrate with a PDF generation library to create and save the report in PDF format.

        Parameters
        ----------
        case : Case
            Case object for which the PDF report will be generated.

        Returns
        -------
        str
            A string indicating the PDF generation of the case.

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> from sentinelresponse.alerts.models import Alert
        >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
        >>> case = Case(case_id=101, title="Incident Investigation")
        >>> case.add_alert(alert)
        >>> reporter = CaseReporter()
        >>> pdf_report = reporter.generate_report_pdf(case)
        >>> print(pdf_report)
        PDF report for case 101

        """
        logging.info(f"Generating PDF report for case {case.case_id}...")
        # Here, you could integrate with an actual PDF generation library.
        return f"PDF report for case {case.case_id}"
