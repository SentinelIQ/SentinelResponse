class User:
    """Represents a user of the system.

    This class encapsulates a system user with a unique identifier, username, and email address.
    It is used by the user management module to perform operations such as creation, retrieval,
    and updates of user information.

    Parameters
    ----------
    user_id : int
        Unique identifier for the user.
    username : str
        The username associated with the user.
    email : str
        The email address of the user.

    Attributes
    ----------
    user_id : int
        Unique identifier for the user.
    username : str
        The username associated with the user.
    email : str
        The email address of the user.

    Examples
    --------
    >>> user = User(user_id=1001, username="johndoe", email="johndoe@example.com")
    >>> print(user)
    User(id=1001, username='johndoe')

    """

    def __init__(self, user_id: int, username: str, email: str):
        """Initialize a new User instance.

        Parameters
        ----------
        user_id : int
            Unique identifier for the user.
        username : str
            The username associated with the user.
        email : str
            The email address of the user.

        """
        self.user_id = user_id
        self.username = username
        self.email = email

    def __repr__(self) -> str:
        """Return the official string representation of the User.

        Returns
        -------
        str
            A string representation of the User, showing its user_id and username.

        Examples
        --------
        >>> user = User(user_id=1001, username="johndoe", email="johndoe@example.com")
        >>> repr(user)
        "User(id=1001, username='johndoe')"

        """
        return f"User(id={self.user_id}, username='{self.username}')"
