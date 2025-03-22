from sentinelresponse.cases.models import Case
from sentinelresponse.logmanager.log_manager import LogManager


class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str):
        super().__init__(message)


class CaseManager:
    """Manages security cases with full CRUD operations.

    Stores Case objects in an internal dictionary keyed by case_id.
    """

    def __init__(self):
        """Initialize a new CaseManager with empty storage."""
        self.cases: dict[int, Case] = {}
        self.logger = LogManager.get_logger()

    def create_case(self, case: Case) -> None:
        """Create a new case and add it to storage."""
        self.logger.info(f"Creating case: {case}")
        self.cases[case.case_id] = case

    def read_case(self, case_id: int) -> Case:
        """Retrieve a case by its unique identifier.

        Raises NotFoundError if not found.
        """
        if case_id in self.cases:
            case = self.cases[case_id]
            self.logger.debug(f"Retrieved case: {case}")
            return case

        message = f"Case {case_id} not found."
        self.logger.warning(message)
        raise NotFoundError(message)

    def read_all_cases(self) -> list[Case]:
        """Retrieve all cases currently stored."""
        cases = list(self.cases.values())
        self.logger.debug(f"Retrieved {len(cases)} cases.")
        return cases

    def update_case(self, case: Case) -> None:
        """Update an existing case.

        Raises NotFoundError if the case does not exist.
        """
        if case.case_id in self.cases:
            self.logger.info(f"Updating case: {case}")
            self.cases[case.case_id] = case
        else:
            message = f"Case {case.case_id} not found for update."
            self.logger.warning(message)
            raise NotFoundError(message)

    def delete_case(self, case_id: int) -> None:
        """Delete a case by its unique identifier.

        Raises NotFoundError if the case does not exist.
        """
        if case_id in self.cases:
            self.logger.info(f"Deleting case id={case_id}")
            del self.cases[case_id]
        else:
            message = f"Case {case_id} not found for deletion."
            self.logger.warning(message)
            raise NotFoundError(message)
