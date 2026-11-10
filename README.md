# Autom for Hermes Agent

Live Google Search results for the built-in web_search tool, through the Autom SERP API.

## Install

```sh
hermes plugins install autom
```

Hermes asks for `AUTOM_API_KEY` during the install. Create a key in the [Autom dashboard](https://app.autom.dev).

Then select it in `hermes tools`, or in `~/.hermes/config.yaml`:

```yaml
web:
  search_backend: autom
```

It is search only, so keep an extract backend for `web_extract`.

## Settings

| Setting | Default | Meaning |
|---|---|---|
| `country` | `us` | 2-letter country code the Google results come from. |
| `language` | (Google's default) | Interface language, for example `en` or `fr`. |

## What it does on your machine

- **Network:** calls `https://api.autom.dev` only, with your `AUTOM_API_KEY`. Calls can use credits on your Autom account ([pricing](https://www.autom.dev/pricing)).
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

## Development

```sh
python -m pytest
```

The tests mock the network and run without Hermes installed.

## Contact

- Source: https://github.com/automdev/hermes-plugin-autom
- Autom: https://www.autom.dev
- Issues: https://github.com/automdev/hermes-plugin-autom/issues

## License

MIT
