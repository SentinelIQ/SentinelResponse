from sentinelresponse.alerts.manager import AlertManager
from sentinelresponse.alerts.models import Alert
from sentinelresponse.cases.manager import CaseManager
from sentinelresponse.cases.models import Case
from sentinelresponse.users.manager import UserManager
from sentinelresponse.users.models import User


class API:
    """API for integration and access to the main modules of the system.

    This class provides a unified interface to perform complete CRUD operations on
    alerts, cases, and users. It acts as a façade over the underlying managers,
    enabling external clients to create, read, update, and delete entities within the system.

    Attributes
    ----------
    alert_manager : AlertManager
        Manager responsible for handling CRUD operations on alerts.
    case_manager : CaseManager
        Manager responsible for handling CRUD operations on cases.
    user_manager : UserManager
        Manager responsible for handling CRUD operations on users.

    """

    def __init__(
        self,
        alert_manager: AlertManager,
        case_manager: CaseManager,
        user_manager: UserManager,
    ):
        """Initialize the API with the provided managers.

        Parameters
        ----------
        alert_manager : AlertManager
            Instance of AlertManager to manage alerts.
        case_manager : CaseManager
            Instance of CaseManager to manage cases.
        user_manager : UserManager
            Instance of UserManager to manage users.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> api = API(AlertManager(), CaseManager(), UserManager())

        """
        self.alert_manager = alert_manager
        self.case_manager = case_manager
        self.user_manager = user_manager

    # Alert CRUD Operations
    def create_alert(self, alert: Alert) -> None:
        """Create a new alert.

        Parameters
        ----------
        alert : Alert
            The Alert object to be created. Its `alert_id` must be unique.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
        >>> api.create_alert(alert)

        """
        self.alert_manager.create_alert(alert)

    def read_alert(self, alert_id: int) -> Alert:
        """Retrieve an alert by its unique identifier.

        Parameters
        ----------
        alert_id : int
            The unique identifier of the alert.

        Returns
        -------
        Alert
            The Alert object with the specified ID.

        Raises
        ------
        NotFoundError
            If the alert with the given ID does not exist.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
        >>> api.create_alert(alert)
        >>> retrieved_alert = api.read_alert(1)
        >>> retrieved_alert.message
        'Suspicious login detected'

        """
        return self.alert_manager.read_alert(alert_id)

    def update_alert(self, alert: Alert) -> None:
        """Update an existing alert.

        Parameters
        ----------
        alert : Alert
            The updated Alert object. Its `alert_id` must correspond to an existing alert.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no alert with the given `alert_id` exists.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> alert = Alert(alert_id=1, message="Initial message", severity="High")
        >>> api.create_alert(alert)
        >>> alert.message = "Updated alert message"
        >>> api.update_alert(alert)

        """
        self.alert_manager.update_alert(alert)

    def delete_alert(self, alert_id: int) -> None:
        """Delete an alert by its unique identifier.

        Parameters
        ----------
        alert_id : int
            The unique identifier of the alert to be deleted.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If the alert with the given ID does not exist.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> alert = Alert(alert_id=1, message="Suspicious login detected", severity="High")
        >>> api.create_alert(alert)
        >>> api.delete_alert(1)

        """
        self.alert_manager.delete_alert(alert_id)

    def get_alerts(self) -> list[Alert]:
        """Retrieve all alerts.

        Returns
        -------
        list[Alert]
            A list of all Alert objects currently managed by the system.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.alerts.models import Alert
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> alert1 = Alert(alert_id=1, message="Alert 1", severity="High")
        >>> alert2 = Alert(alert_id=2, message="Alert 2", severity="Low")
        >>> api.create_alert(alert1)
        >>> api.create_alert(alert2)
        >>> alerts = api.get_alerts()
        >>> len(alerts)
        2

        """
        return self.alert_manager.read_all_alerts()

    # Case CRUD Operations
    def create_case(self, case: Case) -> None:
        """Create a new case.

        Parameters
        ----------
        case : Case
            The Case object to be created. Its `case_id` must be unique.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.cases.models import Case
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> case = Case(case_id=101, title="Investigation Case")
        >>> api.create_case(case)

        """
        self.case_manager.create_case(case)

    def read_case(self, case_id: int) -> Case:
        """Retrieve a case by its unique identifier.

        Parameters
        ----------
        case_id : int
            The unique identifier of the case.

        Returns
        -------
        Case
            The Case object with the specified ID.

        Raises
        ------
        NotFoundError
            If the case with the given ID does not exist.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.cases.models import Case
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> case = Case(case_id=101, title="Investigation Case")
        >>> api.create_case(case)
        >>> retrieved_case = api.read_case(101)
        >>> retrieved_case.title
        'Investigation Case'

        """
        return self.case_manager.read_case(case_id)

    def update_case(self, case: Case) -> None:
        """Update an existing case.

        Parameters
        ----------
        case : Case
            The updated Case object. Its `case_id` must correspond to an existing case.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no case with the given `case_id` exists.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.cases.models import Case
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> case = Case(case_id=101, title="Investigation Case")
        >>> api.create_case(case)
        >>> case.title = "Updated Case Title"
        >>> api.update_case(case)

        """
        self.case_manager.update_case(case)

    def delete_case(self, case_id: int) -> None:
        """Delete a case by its unique identifier.

        Parameters
        ----------
        case_id : int
            The unique identifier of the case to be deleted.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If the case with the given ID does not exist.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.cases.models import Case
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> case = Case(case_id=101, title="Investigation Case")
        >>> api.create_case(case)
        >>> api.delete_case(101)

        """
        self.case_manager.delete_case(case_id)

    def get_cases(self) -> list[Case]:
        """Retrieve all cases.

        Returns
        -------
        list[Case]
            A list of all Case objects currently managed by the system.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.cases.models import Case
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> case1 = Case(case_id=101, title="Investigation Case")
        >>> case2 = Case(case_id=102, title="Another Case")
        >>> api.create_case(case1)
        >>> api.create_case(case2)
        >>> cases = api.get_cases()
        >>> len(cases)
        2

        """
        return self.case_manager.read_all_cases()

    # User CRUD Operations
    def create_user(self, user: User) -> None:
        """Create a new user.

        Parameters
        ----------
        user : User
            The User object to be created. Its `user_id` must be unique.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.users.models import User
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> user = User(user_id=1001, username="analyst1", email="analyst1@example.com")
        >>> api.create_user(user)

        """
        self.user_manager.create_user(user)

    def read_user(self, user_id: int) -> User:
        """Retrieve a user by their unique identifier.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user.

        Returns
        -------
        User
            The User object with the specified ID.

        Raises
        ------
        NotFoundError
            If the user with the given ID does not exist.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.users.models import User
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> user = User(user_id=1001, username="analyst1", email="analyst1@example.com")
        >>> api.create_user(user)
        >>> retrieved_user = api.read_user(1001)
        >>> retrieved_user.username
        'analyst1'

        """
        return self.user_manager.read_user(user_id)

    def update_user(self, user: User) -> None:
        """Update an existing user.

        Parameters
        ----------
        user : User
            The updated User object. Its `user_id` must correspond to an existing user.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no user with the given `user_id` exists.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.users.models import User
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> user = User(user_id=1001, username="analyst1", email="analyst1@example.com")
        >>> api.create_user(user)
        >>> user.username = "updated_username"
        >>> api.update_user(user)

        """
        self.user_manager.update_user(user)

    def delete_user(self, user_id: int) -> None:
        """Delete a user by their unique identifier.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user to be deleted.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If the user with the given ID does not exist.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.users.models import User
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> user = User(user_id=1001, username="analyst1", email="analyst1@example.com")
        >>> api.create_user(user)
        >>> api.delete_user(1001)

        """
        self.user_manager.delete_user(user_id)

    def get_users(self) -> list[User]:
        """Retrieve all users.

        Returns
        -------
        list[User]
            A list of all User objects currently managed by the system.

        Examples
        --------
        >>> from sentinelresponse.alerts.manager import AlertManager
        >>> from sentinelresponse.cases.manager import CaseManager
        >>> from sentinelresponse.users.manager import UserManager
        >>> from sentinelresponse.users.models import User
        >>> api = API(AlertManager(), CaseManager(), UserManager())
        >>> user1 = User(user_id=1001, username="analyst1", email="analyst1@example.com")
        >>> user2 = User(user_id=1002, username="analyst2", email="analyst2@example.com")
        >>> api.create_user(user1)
        >>> api.create_user(user2)
        >>> users = api.get_users()
        >>> len(users)
        2

        """
        return self.user_manager.read_all_users()
