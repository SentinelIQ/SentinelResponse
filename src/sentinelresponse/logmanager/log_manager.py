import logging
import logging.handlers
import threading
from pathlib import Path
from time import time

import sentry_sdk
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

from sentinelresponse.config.sentinel_response_config import SentinelResponseConfig


class _OpenSearchBulkHandler(logging.Handler):
    def __init__(
        self, client: OpenSearch, index: str, batch_size: int, flush_interval: float
    ):
        super().__init__()
        self.client = client
        self.index = index
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._buffer = []
        self._lock = threading.Lock()
        self._last_flush = time()

    def emit(self, record: logging.LogRecord) -> None:
        doc = {
            "_index": self.index,
            "_source": {
                "@timestamp": self.formatter.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "pathname": record.pathname,
                "lineno": record.lineno,
            },
        }
        with self._lock:
            self._buffer.append(doc)
            if (
                len(self._buffer) >= self.batch_size
                or (time() - self._last_flush) >= self.flush_interval
            ):
                self.flush()

    def flush(self) -> None:
        with self._lock:
            if not self._buffer:
                return
            try:
                bulk(self.client, self._buffer)
            except Exception:
                for rec in self._buffer:
                    self.handleError(rec)
            finally:
                self._buffer.clear()
                self._last_flush = time()

    def close(self) -> None:
        try:
            self.flush()
        finally:
            super().close()


class LogManager:
    _logger: logging.Logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            cls._configure_logger()
        return cls._logger

    @classmethod
    def _configure_logger(cls) -> None:
        cfg = SentinelResponseConfig()
        app_name = cfg.main.get("app_name", "app")
        log_cfg = cfg.log

        logger = logging.getLogger(app_name)
        logger.setLevel(log_cfg.get("level", "INFO"))
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
        )

        log_path = Path(log_cfg.get("file", f"{app_name}.log"))
        log_path.parent.mkdir(parents=True, exist_ok=True)

        fh = logging.handlers.RotatingFileHandler(
            filename=log_path,
            maxBytes=int(log_cfg.get("max_size_mb", 100)) * 1024 * 1024,
            backupCount=int(log_cfg.get("backup_count", 3)),
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sentry_dsn = log_cfg.get("sentry_dsn")
        if sentry_dsn:
            sentry_sdk.init(dsn=sentry_dsn)
            logger.addHandler(
                sentry_sdk.integrations.logging.EventHandler(level=logging.ERROR)
            )

        op_cfg = log_cfg.get("opensearch_config", {})
        hosts = op_cfg.get("hosts", [])
        if hosts:
            http_auth = tuple(op_cfg.get("http_auth", [])) or None
            client = OpenSearch(
                hosts=hosts,
                http_auth=http_auth,
                use_ssl=bool(op_cfg.get("use_ssl", False)),
                verify_certs=bool(op_cfg.get("verify_certs", False)),
            )

            index_name = app_name.lower()
            try:
                if not client.indices.exists(index=index_name):
                    client.indices.create(index=index_name)
                    logger.info(f"Created OpenSearch index '{index_name}'")
                else:
                    logger.info(f"OpenSearch index '{index_name}' already exists")
            except Exception as e:
                logger.warning(
                    f"Could not check/create OpenSearch index '{index_name}': {e}"
                )

            osh = _OpenSearchBulkHandler(
                client=client,
                index=index_name,
                batch_size=int(op_cfg.get("batch_size", 100)),
                flush_interval=float(op_cfg.get("flush_interval", 5.0)),
            )
            osh.setFormatter(formatter)
            logger.addHandler(osh)

        cls._logger = logger
