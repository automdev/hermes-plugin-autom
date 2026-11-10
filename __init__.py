"""Autom web search backend for Hermes Agent."""


def register(ctx):
    from .provider import AutomWebSearchProvider

    ctx.register_web_search_provider(AutomWebSearchProvider(ctx))
