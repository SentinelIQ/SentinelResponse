from sentinelresponse.logmanager.log_manager import LogManager
from sentinelresponse.users.models import User


class NotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, message: str):
        super().__init__(message)


class UserManager:
    """Manages users with full CRUD operations.

    This class provides methods to create, read, update, and delete User objects.
    Users are stored in an internal dictionary, keyed by their unique user_id.
    """

    def __init__(self):
        """Initialize the UserManager with an empty dictionary for users."""
        self.users: dict[int, User] = {}
        self.logger = LogManager.get_logger()

    def create_user(self, user: User) -> None:
        """Create a new user and add it to the manager."""
        self.logger.info(f"Creating user: {user}")
        self.users[user.user_id] = user

    def read_user(self, user_id: int) -> User:
        """Retrieve a user by their unique identifier.

        Raises NotFoundError if not found.
        """
        if user_id in self.users:
            return self.users[user_id]

        message = f"User {user_id} not found."
        self.logger.warning(message)
        raise NotFoundError(message)

    def read_all_users(self) -> list[User]:
        """Retrieve all users managed by the UserManager."""
        users = list(self.users.values())
        self.logger.debug(f"Retrieved {len(users)} users")
        return users

    def update_user(self, user: User) -> None:
        """Update an existing user.

        Raises NotFoundError if the user does not exist.
        """
        if user.user_id in self.users:
            self.logger.info(f"Updating user: {user}")
            self.users[user.user_id] = user
        else:
            message = f"User {user.user_id} not found for update."
            self.logger.warning(message)
            raise NotFoundError(message)

    def delete_user(self, user_id: int) -> None:
        """Delete a user by their unique identifier.

        Raises NotFoundError if the user does not exist.
        """
        if user_id in self.users:
            self.logger.info(f"Deleting user id={user_id}")
            del self.users[user_id]
        else:
            message = f"User {user_id} not found for deletion."
            self.logger.warning(message)
            raise NotFoundError(message)
