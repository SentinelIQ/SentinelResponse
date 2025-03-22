import logging

from sentinelresponse.knowledgebase.models import Article


class KnowledgeBase:
    """Manages the knowledge base for storing and retrieving articles.

    This class provides complete CRUD operations for managing articles, where each
    article may optionally be linked to one or more cases and alerts. This design
    enables integration with the rest of the system by associating relevant knowledge
    with specific security cases and alerts.

    Attributes
    ----------
    articles : dict[str, Article]
        A dictionary mapping article titles to their corresponding Article objects.

    Examples
    --------
    >>> kb = KnowledgeBase()
    >>> kb.create_article("Policy", "All incidents must be reported.", [101], [1])
    >>> article = kb.read_article("Policy")
    >>> print(article.linked_cases)
    [101]

    """

    def __init__(self):
        """Initialize the KnowledgeBase with an empty dictionary for articles.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.articles
        {}

        """
        self.articles: dict[str, Article] = {}

    def create_article(
        self,
        title: str,
        content: str,
        linked_cases: list[int] | None = None,
        linked_alerts: list[int] | None = None,
    ) -> None:
        """Create a new article in the knowledge base.

        This method adds a new article to the knowledge base. If an article with the same
        title already exists, it will be overwritten.

        Parameters
        ----------
        title : str
            The title of the article.
        content : str
            The content of the article.
        linked_cases : list[int], optional
            A list of case IDs to be linked with the article. Defaults to an empty list.
        linked_alerts : list[int], optional
            A list of alert IDs to be linked with the article. Defaults to an empty list.

        Returns
        -------
        None

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "All incidents must be reported.", [101, 102], [1, 2])

        """
        logging.info(f"Criando artigo: {title}")
        self.articles[title] = Article(
            title=title,
            content=content,
            linked_cases=linked_cases if linked_cases is not None else [],
            linked_alerts=linked_alerts if linked_alerts is not None else [],
        )

    def read_article(self, title: str) -> Article:
        """Retrieve an article by its title.

        Parameters
        ----------
        title : str
            The title of the article to retrieve.

        Returns
        -------
        Article
            The Article object corresponding to the provided title.

        Raises
        ------
        KeyError
            If the article with the specified title does not exist.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "Content")
        >>> article = kb.read_article("Policy")

        """
        if title in self.articles:
            return self.articles[title]
        raise KeyError(f"Artigo '{title}' não encontrado.")

    def read_all_articles(self) -> dict[str, Article]:
        """Retrieve all articles from the knowledge base.

        Returns
        -------
        dict[str, Article]
            A copy of the dictionary containing all articles, where keys are article titles
            and values are their corresponding Article objects.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "Content")
        >>> all_articles = kb.read_all_articles()
        >>> "Policy" in all_articles
        True

        """
        return self.articles.copy()

    def update_article(
        self,
        title: str,
        new_content: str | None = None,
        new_linked_cases: list[int] | None = None,
        new_linked_alerts: list[int] | None = None,
    ) -> None:
        """Update an existing article's content and linked associations.

        This method updates the content of the article and optionally replaces the lists
        of linked cases and alerts.

        Parameters
        ----------
        title : str
            The title of the article to update.
        new_content : str, optional
            The new content for the article. If None, the content remains unchanged.
        new_linked_cases : list[int], optional
            A new list of case IDs to link with the article. If None, the existing linked cases remain unchanged.
        new_linked_alerts : list[int], optional
            A new list of alert IDs to link with the article. If None, the existing linked alerts remain unchanged.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the article with the specified title does not exist.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "Initial content", [101], [1])
        >>> kb.update_article(
        ...     "Policy",
        ...     new_content="Updated content",
        ...     new_linked_cases=[102],
        ...     new_linked_alerts=[2],
        ... )

        """
        if title in self.articles:
            logging.info(f"Atualizando artigo: {title}")
            article = self.articles[title]
            if new_content is not None:
                article.content = new_content
            if new_linked_cases is not None:
                article.linked_cases = new_linked_cases
            if new_linked_alerts is not None:
                article.linked_alerts = new_linked_alerts
        else:
            raise KeyError(f"Artigo '{title}' não encontrado para atualização.")

    def delete_article(self, title: str) -> None:
        """Delete an article from the knowledge base.

        Parameters
        ----------
        title : str
            The title of the article to delete.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the article with the specified title does not exist.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "Content")
        >>> kb.delete_article("Policy")

        """
        if title in self.articles:
            logging.info(f"Excluindo artigo: {title}")
            del self.articles[title]
        else:
            raise KeyError(f"Artigo '{title}' não encontrado para exclusão.")

    def add_linked_case(self, title: str, case_id: int) -> None:
        """Add a case reference to an existing article.

        This method associates a case with an article by adding the case ID to the article's list
        of linked cases. If the case is already linked, no action is taken.

        Parameters
        ----------
        title : str
            The title of the article to which the case will be linked.
        case_id : int
            The unique identifier of the case to link.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the article with the specified title does not exist.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "Content")
        >>> kb.add_linked_case("Policy", 101)

        """
        if title in self.articles:
            article = self.articles[title]
            if case_id not in article.linked_cases:
                article.linked_cases.append(case_id)
                logging.info(f"Case {case_id} adicionado ao artigo '{title}'")
        else:
            raise KeyError(f"Artigo '{title}' não encontrado para adicionar case.")

    def add_linked_alert(self, title: str, alert_id: int) -> None:
        """Add an alert reference to an existing article.

        This method associates an alert with an article by adding the alert ID to the article's list
        of linked alerts. If the alert is already linked, no action is taken.

        Parameters
        ----------
        title : str
            The title of the article to which the alert will be linked.
        alert_id : int
            The unique identifier of the alert to link.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the article with the specified title does not exist.

        Examples
        --------
        >>> kb = KnowledgeBase()
        >>> kb.create_article("Policy", "Content")
        >>> kb.add_linked_alert("Policy", 1)

        """
        if title in self.articles:
            article = self.articles[title]
            if alert_id not in article.linked_alerts:
                article.linked_alerts.append(alert_id)
                logging.info(f"Alert {alert_id} adicionado ao artigo '{title}'")
        else:
            raise KeyError(f"Artigo '{title}' não encontrado para adicionar alert.")
