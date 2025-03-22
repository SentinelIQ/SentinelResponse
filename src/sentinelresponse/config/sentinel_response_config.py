"""Provides the SentinelResponseConfig class.

This class implements a singleton pattern for managing application configuration
using a TOML file.
"""

import threading
from pathlib import Path

import toml


class SentinelResponseConfig:
    """Class attribute to hold the singleton instance.

    This attribute ensures that only one instance of the `SentinelResponseConfig`
    class exists throughout the application. It is initialized to `None` and
    set to the instance of the class when the `__new__` method is called.

    Notes
    -----
    - The singleton pattern is implemented using a class-level lock (`_lock`)
      to ensure thread safety during instance creation.
    - The `_instance` attribute is checked and updated within a double-checked
      locking mechanism in the `__new__` method.

    Examples
    --------
    >>> config1 = SentinelResponseConfig()
    >>> config2 = SentinelResponseConfig()
    >>> config1 is config2
    True

    """

    _instance = None

    _lock = threading.Lock()
    DEFAULT_PATH = Path(__file__).parent / "config.toml"

    def __new__(cls, toml_path=None):
        """Create or return the singleton instance of the class.

        Parameters
        ----------
        toml_path : str or None, optional
            Path to the TOML configuration file. If None, the default path is used.

        Returns
        -------
        SentinelResponseConfig
            The singleton instance of the SentinelResponseConfig class.

        """
        path = Path(toml_path) if toml_path else cls.DEFAULT_PATH
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._toml_path = path
                    cls._instance._load(path)
        return cls._instance

    def _load(self, toml_path: Path) -> None:
        if not toml_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {toml_path}")
        data = toml.load(toml_path)
        self.main = data.get("main", {})
        self.notification = data.get("notification", {})
        self.log = data.get("log", {})

    def reload(self, toml_path=None) -> None:
        """Reload the configuration from the specified TOML file.

        Parameters
        ----------
        toml_path : str or None, optional
            Path to the TOML configuration file. If None, the previously loaded path is used.

        Raises
        ------
        FileNotFoundError
            If the specified TOML file does not exist.

        """
        path = Path(toml_path) if toml_path else self._toml_path
        self._toml_path = path
        self._load(path)

    def __repr__(self) -> str:
        """Provide a string representation of the SentinelResponseConfig instance.

        Returns
        -------
        str
            A string that includes the main, notification, and log configuration sections.

        """
        return (
            f"<SentinelResponseConfig(main={self.main!r}, "
            f"notification={self.notification!r}, log={self.log!r})>"
        )
