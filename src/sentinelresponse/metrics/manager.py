from sentinelresponse.logmanager.log_manager import LogManager


class MetricsManager:
    """Manages metrics and enables CRUD operations, as well as dynamic dashboard generation.

    This class provides functionality to set, read, update, and delete metrics stored as key-value pairs.
    Each metric is identified by a string key and holds a float value. Additionally, it can generate a simple
    textual dashboard summarizing all stored metrics.

    Attributes
    ----------
    metrics : dict[str, float]
        A dictionary that maps metric names to their corresponding float values.
    """

    def __init__(self):
        """Initialize the MetricsManager with an empty dictionary for metrics."""
        self.metrics: dict[str, float] = {}
        self.logger = LogManager.get_logger()

    def set_metric(self, key: str, value: float) -> None:
        """Set a metric with the specified key and value."""
        self.logger.info(f"Setting metric '{key}' to {value}")
        self.metrics[key] = value

    def read_metric(self, key: str) -> float:
        """Retrieve the value of a metric by its key.

        Raises KeyError if the metric does not exist.
        """
        try:
            return self.metrics[key]
        except KeyError:
            message = f"Metric '{key}' not found."
            self.logger.warning(message)
            raise KeyError(message)

    def read_all_metrics(self) -> dict[str, float]:
        """Retrieve a copy of all metrics."""
        self.logger.debug(f"Retrieving all metrics ({len(self.metrics)})")
        return self.metrics.copy()

    def update_metric(self, key: str, value: float) -> None:
        """Update the value of an existing metric.

        Raises KeyError if the metric does not exist.
        """
        if key in self.metrics:
            self.logger.info(f"Updating metric '{key}' to {value}")
            self.metrics[key] = value
        else:
            message = f"Metric '{key}' not found for update."
            self.logger.warning(message)
            raise KeyError(message)

    def delete_metric(self, key: str) -> None:
        """Delete a metric identified by its key.

        Raises KeyError if the metric does not exist.
        """
        if key in self.metrics:
            self.logger.info(f"Deleting metric '{key}'")
            del self.metrics[key]
        else:
            message = f"Metric '{key}' not found for deletion."
            self.logger.warning(message)
            raise KeyError(message)

    def generate_dashboard(self) -> str:
        """Generate a textual dashboard summarizing all stored metrics."""
        dashboard = "=== Dashboard ===\n"
        for key, value in self.metrics.items():
            dashboard += f"{key}: {value}\n"
        return dashboard.rstrip()
