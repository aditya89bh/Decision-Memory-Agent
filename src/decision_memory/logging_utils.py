import logging
import sys


class TraceFormatter(logging.Formatter):
    """Format log records as compact key-value trace lines."""

    def format(self, record):
        trace_id = getattr(record, "trace_id", "-")
        event = getattr(record, "event", record.getMessage())
        parts = [record.levelname, f"trace_id={trace_id}", f"event={event}"]

        for key, value in sorted(getattr(record, "fields", {}).items()):
            parts.append(f"{key}={value}")

        return " ".join(parts)


def configure_logging():
    """Configure production-style CLI logging using the standard library."""
    logger = logging.getLogger("decision_memory")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(TraceFormatter())
    logger.addHandler(handler)

    return logger


def log_event(logger, trace_id, event, **fields):
    logger.info(event, extra={"trace_id": trace_id, "event": event, "fields": fields})
