"""Unit tests for the Autom plugin. The network is mocked."""

import io
import json
import urllib.error

import hermes_plugin_autom as plugin
import pytest
from hermes_plugin_autom import _client


class FakeContext:
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.providers, self.tools = [], {}

    def get_config(self, key, default=None):
        return self.settings.get(key, default)

    def register_web_search_provider(self, provider):
        self.providers.append(provider)

    def register_tool(self, name, toolset, schema, handler, check_fn=None, **kwargs):
        self.tools[name] = {"toolset": toolset, "schema": schema, "handler": handler, "check_fn": check_fn}


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class Calls(list):
    """Records each request and answers it with the payload given to respond()."""

    def __init__(self, monkeypatch):
        super().__init__()
        self.monkeypatch = monkeypatch

    def respond(self, payload):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            return FakeResponse(json.dumps(payload).encode())

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def fail(self, status, body):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            raise urllib.error.HTTPError(request.full_url, status, "error", {}, io.BytesIO(json.dumps(body).encode()))

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def unreachable(self):
        def urlopen(request, timeout):
            raise urllib.error.URLError("down")

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)


@pytest.fixture
def calls(monkeypatch):
    return Calls(monkeypatch)


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: "test-key" if name == _client.KEY_ENV else default)


@pytest.fixture
def no_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: default)


def query(request):
    return dict(_client.urllib.parse.parse_qsl(_client.urllib.parse.urlsplit(request.full_url).query))


def assert_auth(request):
    assert request.get_header("User-agent").startswith("hermes-plugin-autom/")
    assert request.get_header("X-api-key") == "test-key"


def provider(settings=None):
    ctx = FakeContext(settings)
    plugin.register(ctx)
    return ctx.providers[0]


RESPONSE = {
    "organic_results": [
        {"position": 1, "title": "Hermes Agent", "link": "https://hermes-agent.nousresearch.com", "snippet": "An agent."},
        {"position": 2, "title": "No link", "link": "", "snippet": "Skipped."},
        {"position": 3, "title": "GitHub", "link": "https://github.com/NousResearch/hermes-agent", "snippet": None},
    ]
}


def test_register_adds_a_search_only_provider():
    p = provider()
    assert p.name == "autom"
    assert p.supports_search() is True
    assert p.supports_extract() is False


def test_not_available_without_key(no_key, calls):
    assert provider().is_available() is False
    result = provider().search("hermes")
    assert result["success"] is False and "AUTOM_API_KEY" in result["error"]
    assert calls == []


def test_search_sends_query_country_and_language(api_key, calls):
    calls.respond(RESPONSE)
    provider({"country": "DE", "language": "de"}).search(" hermes agent ")
    request = calls[0]["request"]
    assert request.full_url.startswith("https://api.autom.dev/v1/google/search?")
    assert query(request) == {"query": "hermes agent", "gl": "de", "hl": "de"}
    assert_auth(request)


def test_search_maps_results_and_skips_entries_without_a_link(api_key, calls):
    calls.respond(RESPONSE)
    assert provider().search("hermes", limit=5) == {
        "success": True,
        "data": {
            "web": [
                {"title": "Hermes Agent", "url": "https://hermes-agent.nousresearch.com", "description": "An agent.", "position": 1},
                {"title": "GitHub", "url": "https://github.com/NousResearch/hermes-agent", "description": "", "position": 2},
            ]
        },
    }


def test_search_respects_limit(api_key, calls):
    calls.respond(RESPONSE)
    assert len(provider().search("hermes", limit=1)["data"]["web"]) == 1


def test_invalid_country_fails_without_a_request(api_key, calls):
    result = provider({"country": "Germany"}).search("hermes")
    assert result["success"] is False and "country" in result["error"]
    assert calls == []


def test_empty_query_fails(api_key):
    assert provider().search("  ")["success"] is False


def test_api_error_message_is_returned(api_key, calls):
    calls.fail(401, {"error": "Invalid API Key"})
    assert provider().search("hermes") == {"success": False, "error": "Autom: Invalid API Key"}


def test_network_error(api_key, calls):
    calls.unreachable()
    assert provider().search("hermes") == {"success": False, "error": "Autom: could not reach the API"}


def test_unexpected_response(api_key, calls):
    calls.respond({"something": "else"})
    assert provider().search("hermes")["success"] is False
