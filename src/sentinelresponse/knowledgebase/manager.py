from sentinelresponse.knowledgebase.models import Article
from sentinelresponse.logmanager.log_manager import LogManager


class KnowledgeBase:
    """Manages the knowledge base for storing and retrieving articles.

    Provides full CRUD operations on Article objects, each of which may be linked
    to one or more security cases and alerts.

    Attributes
    ----------
    articles : dict[str, Article]
        Maps article titles to their corresponding Article objects.
    """

    def __init__(self):
        """Initialize an empty knowledge base."""
        self.articles: dict[str, Article] = {}
        self.logger = LogManager.get_logger()

    def create_article(
        self,
        title: str,
        content: str,
        linked_cases: list[int] | None = None,
        linked_alerts: list[int] | None = None,
    ) -> None:
        """Create or overwrite an article in the knowledge base."""
        self.logger.info(f"Creating article '{title}'")
        self.articles[title] = Article(
            title=title,
            content=content,
            linked_cases=linked_cases or [],
            linked_alerts=linked_alerts or [],
        )

    def read_article(self, title: str) -> Article:
        """Retrieve an article by its title."""
        try:
            return self.articles[title]
        except KeyError:
            message = f"Article '{title}' not found."
            self.logger.warning(message)
            raise KeyError(message)

    def read_all_articles(self) -> dict[str, Article]:
        """Return all articles in the knowledge base."""
        self.logger.debug(f"Retrieving all articles ({len(self.articles)})")
        return self.articles.copy()

    def update_article(
        self,
        title: str,
        new_content: str | None = None,
        new_linked_cases: list[int] | None = None,
        new_linked_alerts: list[int] | None = None,
    ) -> None:
        """Update an existing article s content or linked associations."""
        if title not in self.articles:
            message = f"Article '{title}' not found for update."
            self.logger.warning(message)
            raise KeyError(message)

        article = self.articles[title]
        self.logger.info(f"Updating article '{title}'")
        if new_content is not None:
            article.content = new_content
        if new_linked_cases is not None:
            article.linked_cases = new_linked_cases
        if new_linked_alerts is not None:
            article.linked_alerts = new_linked_alerts

    def delete_article(self, title: str) -> None:
        """Delete an article by its title."""
        if title not in self.articles:
            message = f"Article '{title}' not found for deletion."
            self.logger.warning(message)
            raise KeyError(message)

        self.logger.info(f"Deleting article '{title}'")
        del self.articles[title]

    def add_linked_case(self, title: str, case_id: int) -> None:
        """Associate a case ID with an existing article."""
        if title not in self.articles:
            message = f"Article '{title}' not found for linking case."
            self.logger.warning(message)
            raise KeyError(message)

        article = self.articles[title]
        if case_id not in article.linked_cases:
            article.linked_cases.append(case_id)
            self.logger.info(f"Linked case {case_id} to article '{title}'")

    def add_linked_alert(self, title: str, alert_id: int) -> None:
        """Associate an alert ID with an existing article."""
        if title not in self.articles:
            message = f"Article '{title}' not found for linking alert."
            self.logger.warning(message)
            raise KeyError(message)

        article = self.articles[title]
        if alert_id not in article.linked_alerts:
            article.linked_alerts.append(alert_id)
            self.logger.info(f"Linked alert {alert_id} to article '{title}'")
