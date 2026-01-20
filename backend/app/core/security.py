import time

from fastapi import HTTPException

from app.core.config import settings

_request_log: dict[str, list[float]] = {}


def sanitize_query(query: str) -> str:
    return (query or "").strip()


def enforce_rate_limit(client_id: str) -> None:
    if not client_id:
        raise HTTPException(status_code=400, detail="client_id is required.")
    now = time.time()
    window_start = now - 60
    timestamps = _request_log.setdefault(client_id, [])
    _request_log[client_id] = [t for t in timestamps if t >= window_start]
    if len(_request_log[client_id]) >= settings.max_requests_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    _request_log[client_id].append(now)
