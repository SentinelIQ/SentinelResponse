import logging

from sentinelresponse.users.models import User


class NotFoundError(Exception):
    """Exception raised when a user is not found.

    This exception is used by the UserManager methods to indicate that a user with a specific
    identifier does not exist in the internal storage.

    Examples
    --------
    >>> try:
    ...     raise NotFoundError("Usuário 1 não encontrado.")
    ... except NotFoundError as e:
    ...     print(e)
    Usuário 1 não encontrado.

    """


class UserManager:
    """Manages users with full CRUD operations.

    This class provides methods to create, read, update, and delete User objects.
    Users are stored in an internal dictionary, keyed by their unique user_id.

    Attributes
    ----------
    users : dict[int, User]
        A dictionary mapping user IDs to User objects.

    Examples
    --------
    >>> from sentinelresponse.users.models import User
    >>> manager = UserManager()
    >>> user = User(user_id=1001, username="analyst", email="analyst@example.com")
    >>> manager.create_user(user)
    >>> print(manager.read_user(1001))
    User(id=1001, username='analyst')

    """

    def __init__(self):
        """Initialize the UserManager with an empty dictionary for users.

        Examples
        --------
        >>> um = UserManager()
        >>> um.users
        {}

        """
        self.users: dict[int, User] = {}

    def create_user(self, user: User) -> None:
        """Create a new user and add it to the manager.

        This method logs the creation of a new user and stores the User object in the
        internal dictionary using the user's unique user_id as the key.

        Parameters
        ----------
        user : User
            The User object to be created. Its user_id should be unique.

        Returns
        -------
        None

        Examples
        --------
        >>> from sentinelresponse.users.models import User
        >>> um = UserManager()
        >>> user = User(user_id=1001, username="analyst", email="analyst@example.com")
        >>> um.create_user(user)

        """
        logging.info(f"Criando usuário: {user}")
        self.users[user.user_id] = user

    def read_user(self, user_id: int) -> User:
        """Retrieve a user by their unique identifier.

        This method searches the internal dictionary for a User with the provided user_id.
        If found, the User object is returned; otherwise, a NotFoundError is raised.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user to retrieve.

        Returns
        -------
        User
            The User object associated with the given user_id.

        Raises
        ------
        NotFoundError
            If no user with the specified user_id exists.

        Examples
        --------
        >>> from sentinelresponse.users.models import User
        >>> um = UserManager()
        >>> user = User(user_id=1001, username="analyst", email="analyst@example.com")
        >>> um.create_user(user)
        >>> user_retrieved = um.read_user(1001)
        >>> print(user_retrieved)
        User(id=1001, username='analyst')

        """
        if user_id in self.users:
            return self.users[user_id]
        raise NotFoundError(f"Usuário {user_id} não encontrado.")

    def read_all_users(self) -> list[User]:
        """Retrieve all users managed by the UserManager.

        Returns
        -------
        list[User]
            A list of all User objects stored in the manager.

        Examples
        --------
        >>> um = UserManager()
        >>> # Assume some users have been added
        >>> all_users = um.read_all_users()

        """
        return list(self.users.values())

    def update_user(self, user: User) -> None:
        """Update an existing user in the manager.

        This method replaces the User object in the internal dictionary with the provided
        updated User object. The user_id of the updated user must already exist.

        Parameters
        ----------
        user : User
            The updated User object. Its user_id must correspond to an existing user.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no user with the given user_id exists in the manager.

        Examples
        --------
        >>> um = UserManager()
        >>> user = User(user_id=1001, username="analyst", email="analyst@example.com")
        >>> um.create_user(user)
        >>> user.username = "senior_analyst"
        >>> um.update_user(user)

        """
        if user.user_id in self.users:
            logging.info(f"Atualizando usuário: {user}")
            self.users[user.user_id] = user
        else:
            raise NotFoundError(
                f"Usuário {user.user_id} não encontrado para atualização."
            )

    def delete_user(self, user_id: int) -> None:
        """Delete a user by their unique identifier.

        This method removes the User object associated with the provided user_id from the
        internal dictionary. If the user does not exist, a NotFoundError is raised.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user to delete.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If no user with the specified user_id exists.

        Examples
        --------
        >>> from sentinelresponse.users.models import User
        >>> um = UserManager()
        >>> user = User(user_id=1001, username="analyst", email="analyst@example.com")
        >>> um.create_user(user)
        >>> um.delete_user(1001)

        """
        if user_id in self.users:
            logging.info(f"Excluindo usuário com ID: {user_id}")
            del self.users[user_id]
        else:
            raise NotFoundError(f"Usuário {user_id} não encontrado para exclusão.")
