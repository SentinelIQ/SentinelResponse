from datetime import datetime

from sentinelresponse.logmanager.log_manager import LogManager


class TimelineManager:
    """Manages a timeline of events, supporting CRUD operations on events.

    Each event is represented as a tuple consisting of a timestamp and a description.
    This class allows for creating, reading, updating, and deleting events while
    maintaining a sorted order based on the event timestamps.
    """

    def __init__(self):
        """Initialize the TimelineManager with an empty list of events."""
        self.events: list[tuple[datetime, str]] = []
        self.logger = LogManager.get_logger()

    def create_event(self, timestamp: datetime, description: str) -> None:
        """Create a new event and add it to the timeline."""
        self.logger.info(f"Adding event '{description}' at {timestamp}")
        self.events.append((timestamp, description))

    def read_events(self) -> list[tuple[datetime, str]]:
        """Retrieve all events sorted by timestamp."""
        return sorted(self.events, key=lambda event: event[0])

    def update_event(self, index: int, timestamp: datetime, description: str) -> None:
        """Update an existing event at the specified index.

        Raises IndexError if the index is out of range.
        """
        if 0 <= index < len(self.events):
            self.logger.info(f"Updating event at index {index}")
            self.events[index] = (timestamp, description)
        else:
            message = "Event not found for update."
            self.logger.warning(message)
            raise IndexError(message)

    def delete_event(self, index: int) -> None:
        """Delete an event from the timeline at the specified index.

        Raises IndexError if the index is out of range.
        """
        if 0 <= index < len(self.events):
            self.logger.info(f"Deleting event at index {index}")
            del self.events[index]
        else:
            message = "Event not found for deletion."
            self.logger.warning(message)
            raise IndexError(message)
