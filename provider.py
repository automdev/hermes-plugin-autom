"""Adapt Autom's Google Search response to the Hermes web_search contract."""

from __future__ import annotations

import re

from agent.web_search_provider import WebSearchProvider

from . import _client


def _failure(message):
    return {"success": False, "error": f"Autom: {message}"}


def _results(data, limit):
    items = data.get("organic_results") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError("response must contain organic_results")
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        url = item.get("link")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        title = item.get("title")
        snippet = item.get("snippet")
        rows.append(
            {
                "title": title if isinstance(title, str) else "",
                "url": url,
                "description": snippet if isinstance(snippet, str) else "",
                "position": len(rows) + 1,
            }
        )
        if len(rows) >= limit:
            break
    return {"success": True, "data": {"web": rows}}


class AutomWebSearchProvider(WebSearchProvider):
    """Search only: live Google organic results. Pair it with an extract backend for web_extract."""

    def __init__(self, ctx):
        # Read settings on every call: one process can serve several profiles.
        self._get_config = ctx.get_config

    @property
    def name(self):
        return "autom"

    @property
    def display_name(self):
        return "Autom (Google Search)"

    def _setting(self, key, default, pattern, label):
        value = self._get_config(key, default)
        value = value.strip().lower() if isinstance(value, str) else ""
        if value and not re.fullmatch(pattern, value):
            raise ValueError(f"{key} must be {label}")
        return value

    def is_available(self):
        return bool(_client.api_key())

    def get_setup_schema(self):
        return {
            "name": self.display_name,
            "badge": "paid",
            "tag": "Live Google results. Search only.",
            "env_vars": [{"key": _client.KEY_ENV, "prompt": "Autom API key", "url": "https://app.autom.dev"}],
        }

    def search(self, query, limit=5):
        if not isinstance(query, str) or not query.strip():
            return _failure("query must not be empty")
        try:
            country = self._setting("country", "us", r"[a-z]{2}", "a 2-letter country code, for example us")
            language = self._setting("language", "", r"[a-z]{2,3}(-[a-z]{2,4})?", "a language code, for example en")
            data = _client.get("/v1/google/search", {"query": query.strip(), "gl": country, "hl": language})
            return _results(data, max(1, int(limit)))
        except (ValueError, _client.ApiError) as exc:
            return _failure(str(exc))
