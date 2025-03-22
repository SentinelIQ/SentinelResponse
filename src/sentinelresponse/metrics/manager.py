import logging


class MetricsManager:
    """Manages metrics and enables CRUD operations, as well as dynamic dashboard generation.

    This class provides functionality to set, read, update, and delete metrics stored as key-value pairs.
    Each metric is identified by a string key and holds a float value. Additionally, it can generate a simple
    textual dashboard summarizing all stored metrics.

    Attributes
    ----------
    metrics : dict[str, float]
        A dictionary that maps metric names to their corresponding float values.

    Examples
    --------
    >>> mm = MetricsManager()
    >>> mm.set_metric("accuracy", 0.95)
    >>> mm.read_metric("accuracy")
    0.95
    >>> print(mm.generate_dashboard())
    === Dashboard ===
    accuracy: 0.95

    """

    def __init__(self):
        """Initialize the MetricsManager with an empty dictionary for metrics.

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.metrics
        {}

        """
        self.metrics: dict[str, float] = {}

    def set_metric(self, key: str, value: float) -> None:
        """Set a metric with the specified key and value.

        If a metric with the given key already exists, it is overwritten.

        Parameters
        ----------
        key : str
            The name of the metric.
        value : float
            The value to assign to the metric.

        Returns
        -------
        None

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.set_metric("accuracy", 0.95)
        >>> mm.metrics["accuracy"]
        0.95

        """
        logging.info(f"Definindo métrica '{key}' com valor {value}")
        self.metrics[key] = value

    def read_metric(self, key: str) -> float:
        """Retrieve the value of a metric by its key.

        Parameters
        ----------
        key : str
            The name of the metric to retrieve.

        Returns
        -------
        float
            The value associated with the specified metric.

        Raises
        ------
        KeyError
            If the metric with the specified key does not exist.

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.set_metric("accuracy", 0.95)
        >>> mm.read_metric("accuracy")
        0.95

        """
        if key in self.metrics:
            return self.metrics[key]
        raise KeyError(f"Métrica '{key}' não encontrada.")

    def read_all_metrics(self) -> dict[str, float]:
        """Retrieve a copy of all metrics.

        Returns
        -------
        dict[str, float]
            A dictionary containing all metrics stored in the manager.

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.set_metric("accuracy", 0.95)
        >>> mm.read_all_metrics()
        {'accuracy': 0.95}

        """
        return self.metrics.copy()

    def update_metric(self, key: str, value: float) -> None:
        """Update the value of an existing metric.

        Parameters
        ----------
        key : str
            The name of the metric to update.
        value : float
            The new value for the metric.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the metric with the specified key is not found.

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.set_metric("accuracy", 0.95)
        >>> mm.update_metric("accuracy", 0.97)
        >>> mm.read_metric("accuracy")
        0.97

        """
        if key in self.metrics:
            logging.info(f"Atualizando métrica '{key}' para {value}")
            self.metrics[key] = value
        else:
            raise KeyError(f"Métrica '{key}' não encontrada para atualização.")

    def delete_metric(self, key: str) -> None:
        """Delete a metric identified by its key.

        Parameters
        ----------
        key : str
            The name of the metric to delete.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the metric with the specified key does not exist.

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.set_metric("accuracy", 0.95)
        >>> mm.delete_metric("accuracy")
        >>> "accuracy" in mm.metrics
        False

        """
        if key in self.metrics:
            logging.info(f"Excluindo métrica '{key}'")
            del self.metrics[key]
        else:
            raise KeyError(f"Métrica '{key}' não encontrada para exclusão.")

    def generate_dashboard(self) -> str:
        """Generate a textual dashboard summarizing all stored metrics.

        Returns
        -------
        str
            A formatted string listing all metric keys and their values.

        Examples
        --------
        >>> mm = MetricsManager()
        >>> mm.set_metric("accuracy", 0.95)
        >>> print(mm.generate_dashboard())
        === Dashboard ===
        accuracy: 0.95

        """
        dashboard = "=== Dashboard ===\n"
        for key, value in self.metrics.items():
            dashboard += f"{key}: {value}\n"
        return dashboard.rstrip()
