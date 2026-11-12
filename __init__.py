"""Autom for Hermes Agent: a web_search backend plus tools for Google, Bing, Brave, DuckDuckGo and Yahoo."""


def register(ctx):
    from . import _client
    from .provider import AutomWebSearchProvider
    from .schemas import TOOLS
    from .tools import handler

    ctx.register_web_search_provider(AutomWebSearchProvider(ctx))

    def available():
        return bool(_client.api_key())

    for name, (description, parameters, *_rest) in TOOLS.items():
        ctx.register_tool(
            name=name,
            toolset="autom",
            schema={"name": name, "description": description, "parameters": parameters},
            handler=handler(name),
            check_fn=available,
        )
