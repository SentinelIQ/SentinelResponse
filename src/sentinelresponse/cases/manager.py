import logging

from sentinelresponse.cases.models import Case


class NotFoundError(Exception):
    """Exception raised when an item is not found.

    This exception is used to indicate that a requested Case was not found in
    the CaseManager's storage.

    Examples
    --------
    >>> try:
    ...     raise NotFoundError("Caso 101 não encontrado.")
    ... except NotFoundError as e:
    ...     print(e)
    Caso 101 não encontrado.

    """


class CaseManager:
    """Manages security cases with full CRUD operations.

    This class provides methods to create, read, update, and delete Case objects.
    Cases are stored internally in a dictionary, keyed by their unique identifier.

    Attributes
    ----------
    cases : dict[int, Case]
        A dictionary mapping each case's unique identifier to its corresponding
        Case object.

    Examples
    --------
    >>> from sentinelresponse.cases.models import Case
    >>> manager = CaseManager()
    >>> case = Case(case_id=101, title="Investigação de Incidente")
    >>> manager.create_case(case)
    >>> retrieved_case = manager.read_case(101)

    """

    def __init__(self):
        """Initialize a new CaseManager with an empty dictionary for cases.

        The internal storage is a dictionary that maps case IDs to Case objects.

        Examples
        --------
        >>> manager = CaseManager()
        >>> print(manager.cases)
        {}

        """
        self.cases: dict[int, Case] = {}

    def create_case(self, case: Case) -> None:
        """Create a new case and add it to the manager.

        This method logs the creation process and stores the provided Case
        object in the internal dictionary using its unique case_id.

        Parameters
        ----------
        case : Case
            The Case object to be created. The case_id attribute must be unique.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> case = Case(case_id=101, title="Investigação de Incidente")
        >>> manager = CaseManager()
        >>> manager.create_case(case)

        """
        logging.info(f"Criando caso: {case}")
        self.cases[case.case_id] = case

    def read_case(self, case_id: int) -> Case:
        """Retrieve a case by its unique identifier.

        This method searches the internal dictionary for a Case with the given
        case_id. If the case is found, it is returned; otherwise, a NotFoundError
        is raised.

        Parameters
        ----------
        case_id : int
            The unique identifier of the case to retrieve.

        Returns
        -------
        Case
            The Case object associated with the given case_id.

        Raises
        ------
        NotFoundError
            If no case with the provided case_id is found.

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> case = Case(case_id=101, title="Investigação de Incidente")
        >>> manager = CaseManager()
        >>> manager.create_case(case)
        >>> retrieved_case = manager.read_case(101)

        """
        if case_id in self.cases:
            return self.cases[case_id]
        raise NotFoundError(f"Caso {case_id} não encontrado.")

    def read_all_cases(self) -> list[Case]:
        """Retrieve all cases stored in the manager.

        Returns
        -------
        list[Case]
            A list of all Case objects currently managed by the CaseManager.

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> case1 = Case(case_id=101, title="Caso 1")
        >>> case2 = Case(case_id=102, title="Caso 2")
        >>> manager = CaseManager()
        >>> manager.create_case(case1)
        >>> manager.create_case(case2)
        >>> all_cases = manager.read_all_cases()
        >>> len(all_cases)
        2

        """
        return list(self.cases.values())

    def update_case(self, case: Case) -> None:
        """Update an existing case in the manager.

        This method replaces the current Case object in the internal dictionary
        with the updated one provided. The case_id of the provided Case must
        already exist in the storage.

        Parameters
        ----------
        case : Case
            The updated Case object. Its case_id should match an existing case.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no case with the given case_id exists in the manager.

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> case = Case(case_id=101, title="Caso Original")
        >>> manager = CaseManager()
        >>> manager.create_case(case)
        >>> case.title = "Caso Atualizado"
        >>> manager.update_case(case)

        """
        if case.case_id in self.cases:
            logging.info(f"Atualizando caso: {case}")
            self.cases[case.case_id] = case
        else:
            raise NotFoundError(f"Caso {case.case_id} não encontrado para atualização.")

    def delete_case(self, case_id: int) -> None:
        """Delete a case from the manager by its unique identifier.

        This method removes the Case object associated with the provided
        case_id from the internal dictionary. If the case is not found, a
        NotFoundError is raised.

        Parameters
        ----------
        case_id : int
            The unique identifier of the case to delete.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no case with the given case_id exists in the manager.

        Examples
        --------
        >>> from sentinelresponse.cases.models import Case
        >>> case = Case(case_id=101, title="Caso a ser deletado")
        >>> manager = CaseManager()
        >>> manager.create_case(case)
        >>> manager.delete_case(101)

        """
        if case_id in self.cases:
            logging.info(f"Excluindo caso com ID: {case_id}")
            del self.cases[case_id]
        else:
            raise NotFoundError(f"Caso {case_id} não encontrado para exclusão.")
