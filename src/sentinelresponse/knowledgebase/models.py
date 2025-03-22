from dataclasses import dataclass, field


@dataclass
class Article:
    """Represents an article in the knowledge base.

    This article can optionally be linked to one or more cases and alerts.
    These links allow the article to serve as a central repository of information,
    integrating knowledge with specific cases and alerts.

    Attributes
    ----------
    title : str
        The title of the article.
    content : str
        The main content of the article.
    linked_cases : List[int]
        A list of case IDs that are linked to this article.
    linked_alerts : List[int]
        A list of alert IDs that are linked to this article.

    Examples
    --------
    >>> article = Article(
    ...     title="Security Policy",
    ...     content="All incidents must be reported.",
    ...     linked_cases=[101, 102],
    ...     linked_alerts=[1, 2],
    ... )
    >>> print(article)
    Article(title='Security Policy', content='All incidents must be reported.', linked_cases=[101, 102], linked_alerts=[1, 2])

    """

    title: str
    content: str
    linked_cases: list[int] = field(default_factory=list)
    linked_alerts: list[int] = field(default_factory=list)
