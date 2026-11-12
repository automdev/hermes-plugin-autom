"""Tool handlers: each one calls the Autom API and returns a JSON string, errors included."""

from __future__ import annotations

import json
import urllib.parse

from . import _client
from .schemas import TOOLS


def _arguments(name, args):
    """Split the model's arguments into the request path, query parameters and JSON body."""
    _, schema, route, mapping, fixed, _cost, _group = TOOLS[name]
    method, path = route.split(" ", 1)
    values, path_values = dict(fixed), {}
    for arg, value in (args or {}).items():
        if value is None or value == "" or arg not in mapping:
            continue
        api_name = mapping[arg]
        if "{" + api_name + "}" in path:
            path_values[api_name] = urllib.parse.quote(str(value).strip(), safe="")
        else:
            values[api_name] = value
    for arg in schema.get("required", []):
        if mapping.get(arg) not in values and mapping.get(arg) not in path_values:
            raise ValueError(f"{arg} is required")
    path = path.format(**path_values)
    if method == "GET":
        params = {k: json.dumps(v, separators=(",", ":")) if isinstance(v, (dict, list)) else v for k, v in values.items()}
        return method, path, params, None
    return method, path, None, values


def call(name, args):
    try:
        method, path, params, body = _arguments(name, args)
        return json.dumps(_client.request(method, path, params, body), ensure_ascii=False)
    except (ValueError, KeyError, _client.ApiError) as exc:
        return json.dumps({"error": f"Autom: {exc}"})


def handler(name):
    def run(args, **kwargs):
        return call(name, args)

    run.__name__ = name
    return run
