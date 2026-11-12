"""Unit tests for the Autom tools. The network is mocked."""

import io
import json
import urllib.error
from pathlib import Path

import hermes_plugin_autom as plugin
import pytest
from hermes_plugin_autom import _client
from hermes_plugin_autom.schemas import TOOLS


class FakeContext:
    def __init__(self):
        self.providers, self.tools = [], {}

    def get_config(self, key, default=None):
        return default

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

    def respond(self, payload=None, status=None):
        def urlopen(request, timeout):
            self.append(request)
            if status:
                raise urllib.error.HTTPError(request.full_url, status, "error", {}, io.BytesIO(json.dumps(payload).encode()))
            return FakeResponse(json.dumps(payload).encode())

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


def tools():
    ctx = FakeContext()
    plugin.register(ctx)
    return ctx.tools


def run(name, args):
    return json.loads(tools()[name]["handler"](args))


def query(request):
    return dict(_client.urllib.parse.parse_qsl(_client.urllib.parse.urlsplit(request.full_url).query))


def test_register_adds_every_tool_in_one_toolset():
    registered = tools()
    assert set(registered) >= set(TOOLS)
    assert {t["toolset"] for t in registered.values()} == {"autom"}
    for name, tool in registered.items():
        assert tool["schema"]["name"] == name
        assert tool["schema"]["parameters"]["type"] == "object"
        assert set(tool["schema"]["parameters"]["required"]) <= set(tool["schema"]["parameters"]["properties"])


def test_manifest_lists_every_tool():
    manifest = (Path(__file__).resolve().parents[1] / "plugin.yaml").read_text()
    listed = {line.strip()[2:] for line in manifest.splitlines() if line.strip().startswith("- autom_")}
    assert listed == set(tools())


def test_tools_hidden_without_key(no_key):
    assert all(tool["check_fn"]() is False for tool in tools().values())


def test_every_description_names_what_it_returns():
    for name, (description, *_rest) in TOOLS.items():
        assert len(description) > 40, name


def test_tool_sends_arguments_and_returns_the_api_json(api_key, calls):
    calls.respond({"ok": True})
    result = run('autom_google_search', {'query': 'web scraping api', 'gl': 'fr', 'page': 2})
    request = calls[0]
    assert request.full_url.startswith(_client.BASE_URL + '/v1/google/search')
    assert request.get_method() == 'GET'
    assert request.get_header("X-api-key") == "test-key"
    assert request.get_header("User-agent").startswith("hermes-plugin-autom/")
    assert query(request) == {'query': 'web scraping api', 'gl': 'fr', 'page': '2'}
    assert result == {"ok": True}


def test_empty_arguments_are_left_out(api_key, calls):
    calls.respond({})
    args = dict({'query': 'web scraping api', 'gl': 'fr', 'page': 2})
    optional = [p for p in TOOLS['autom_google_search'][1]["properties"] if p not in args]
    args.update({p: "" for p in optional[:2]})
    run('autom_google_search', args)
    sent = query(calls[0]) if calls[0].data is None else json.loads(calls[0].data)
    assert not any(value == "" for value in sent.values())


@pytest.mark.parametrize("name", [n for n, t in TOOLS.items() if t[1]["required"]])
def test_required_inputs_are_checked_before_any_request(api_key, calls, name):
    calls.respond({})
    result = run(name, {})
    assert result["error"].startswith("Autom: ") and "is required" in result["error"]
    assert calls == []


def test_api_error_message_goes_back_to_the_model(api_key, calls):
    calls.respond({"error": {"message": "Not enough credits"}}, status=402)
    assert run('autom_google_search', {'query': 'web scraping api', 'gl': 'fr', 'page': 2}) == {"error": "Autom: Not enough credits"}


def test_unreachable_api(api_key, monkeypatch):
    def urlopen(request, timeout):
        raise urllib.error.URLError("down")

    monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)
    assert run('autom_google_search', {'query': 'web scraping api', 'gl': 'fr', 'page': 2}) == {"error": "Autom: could not reach the API"}


def test_without_key_no_request_is_sent(no_key, calls):
    result = run('autom_google_search', {'query': 'web scraping api', 'gl': 'fr', 'page': 2})
    assert "AUTOM_API_KEY" in result["error"]
    assert calls == []
