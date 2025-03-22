import logging
from datetime import datetime


class TimelineManager:
    """Manages a timeline of events, supporting CRUD operations on events.

    Each event is represented as a tuple consisting of a timestamp and a description.
    This class allows for creating, reading, updating, and deleting events while
    maintaining a sorted order based on the event timestamps.

    Attributes
    ----------
    events : list[tuple[datetime, str]]
        A list of events, where each event is a tuple (timestamp, description).

    Examples
    --------
    >>> tm = TimelineManager()
    >>> from datetime import datetime
    >>> tm.create_event(datetime(2023, 3, 15, 12, 0), "System started")
    >>> tm.create_event(datetime(2023, 3, 15, 12, 30), "User logged in")
    >>> events = tm.read_events()
    >>> len(events)
    2

    """

    def __init__(self):
        """Initialize the TimelineManager with an empty list of events.

        Examples
        --------
        >>> tm = TimelineManager()
        >>> tm.events
        []

        """
        self.events: list[tuple[datetime, str]] = []

    def create_event(self, timestamp: datetime, description: str) -> None:
        """Create a new event and add it to the timeline.

        The event is represented as a tuple (timestamp, description) and appended to the
        internal list of events.

        Parameters
        ----------
        timestamp : datetime
            The timestamp of the event.
        description : str
            A description of the event.

        Returns
        -------
        None

        Examples
        --------
        >>> from datetime import datetime
        >>> tm = TimelineManager()
        >>> tm.create_event(datetime(2023, 3, 15, 12, 0), "System started")

        """
        logging.info(f"Adicionando evento: '{description}' em {timestamp}")
        self.events.append((timestamp, description))

    def read_events(self) -> list[tuple[datetime, str]]:
        """Retrieve all events sorted by timestamp.

        The events are returned in ascending order based on their timestamp.

        Returns
        -------
        list[tuple[datetime, str]]
            A list of events sorted by timestamp.

        Examples
        --------
        >>> from datetime import datetime
        >>> tm = TimelineManager()
        >>> tm.create_event(datetime(2023, 3, 15, 12, 30), "User logged in")
        >>> tm.create_event(datetime(2023, 3, 15, 12, 0), "System started")
        >>> events = tm.read_events()
        >>> events[0][1]
        'System started'

        """
        return sorted(self.events, key=lambda event: event[0])

    def update_event(self, index: int, timestamp: datetime, description: str) -> None:
        """Update an existing event at the specified index.

        This method replaces the event at the given index with a new event tuple consisting
        of the provided timestamp and description.

        Parameters
        ----------
        index : int
            The index of the event to update.
        timestamp : datetime
            The new timestamp for the event.
        description : str
            The new description for the event.

        Returns
        -------
        None

        Raises
        ------
        IndexError
            If the index is out of the valid range of the events list.

        Examples
        --------
        >>> from datetime import datetime
        >>> tm = TimelineManager()
        >>> tm.create_event(datetime(2023, 3, 15, 12, 0), "System started")
        >>> tm.update_event(0, datetime(2023, 3, 15, 12, 5), "System booted")

        """
        if 0 <= index < len(self.events):
            logging.info(f"Atualizando evento no índice {index}")
            self.events[index] = (timestamp, description)
        else:
            raise IndexError("Evento não encontrado para atualização.")

    def delete_event(self, index: int) -> None:
        """Delete an event from the timeline at the specified index.

        Removes the event tuple located at the given index from the internal events list.

        Parameters
        ----------
        index : int
            The index of the event to delete.

        Returns
        -------
        None

        Raises
        ------
        IndexError
            If the index is out of the valid range of the events list.

        Examples
        --------
        >>> from datetime import datetime
        >>> tm = TimelineManager()
        >>> tm.create_event(datetime(2023, 3, 15, 12, 0), "System started")
        >>> tm.delete_event(0)
        >>> len(tm.events)
        0

        """
        if 0 <= index < len(self.events):
            logging.info(f"Excluindo evento no índice {index}")
            del self.events[index]
        else:
            raise IndexError("Evento não encontrado para exclusão.")
