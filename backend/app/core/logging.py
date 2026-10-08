import logging
import re
import sys
from typing import Any
from backend.app.core.config import settings


class SecretMaskingFilter(logging.Filter):
    """Filter that sanitizes sensitive information from log records."""

    PATTERNS = [
        # Match passwords in URLs/params e.g. postgresql://user:pass@host
        (r"://([^:]+):([^@]+)@", r"://\1:***MASKED***@"),
        # Match key=value secrets e.g. password=xyz, token=abc, secret=123
        (r"(password|passwd|token|secret|api_key|rtsp_pass)=([^\s&]+)", r"\1=***MASKED***"),
        # Match Bearer tokens
        (r"(Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*", r"\1***MASKED***"),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.mask_secrets(record.msg)
        if record.args:
            masked_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    masked_args.append(self.mask_secrets(arg))
                else:
                    masked_args.append(arg)
            record.args = tuple(masked_args)
        return True

    @classmethod
    def mask_secrets(cls, text: str) -> str:
        masked = text
        for pattern, replacement in cls.PATTERNS:
            masked = re.sub(pattern, replacement, masked, flags=re.IGNORECASE)
        return masked


def setup_logging() -> logging.Logger:
    """Configures structured backend logging with security filtering."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    log_format = (
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"
    )
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SecretMaskingFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to prevent duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    root_logger.addHandler(console_handler)

    app_logger = logging.getLogger("visionforge")
    app_logger.setLevel(log_level)

    return app_logger


logger = setup_logging()
