# Autom for Hermes Agent

Live search engine results for [Hermes Agent](https://hermes-agent.nousresearch.com), through the [Autom](https://www.autom.dev) SERP API.

- **17 tools** for Google (Search, News, Images, Videos, Shopping, Maps, Autocomplete), Bing, Brave (web, images, videos), DuckDuckGo and Yahoo, each returning clean JSON.
- **One fallback search** (`autom_search`) that tries several engines in turn, so the agent still gets results when one engine fails.
- **A backend for the built-in `web_search` tool**, so every search Hermes runs uses live Google results.

## Contents

- [Install](#install)
- [How it works](#how-it-works)
- [Tools](#tools)
- [Use it as the web_search backend](#use-it-as-the-web_search-backend)
- [Choosing country, language and location](#choosing-country-language-and-location)
- [Example prompts](#example-prompts)
- [Credits and errors](#credits-and-errors)
- [What it does on your machine](#what-it-does-on-your-machine)

## Install

```sh
hermes plugins install autom
```

Hermes asks for `AUTOM_API_KEY` during the install. Create a key in the [Autom dashboard](https://app.autom.dev).

Answer yes to `Enable 'autom' now?`, or run `hermes plugins enable autom` later. The tools join the `autom` toolset, which is on by default; turn it on or off in `hermes tools` like any other toolset. They stay hidden from the model until the API key is set.

## How it works

Each tool is one HTTPS call to `https://api.autom.dev`, authenticated with your key. Autom runs the search on the engine live, at the time of the call, parses the results page and sends back JSON: organic results with title, link, snippet and position, plus what the engine shows around them (knowledge graph, news dates, prices, places…). Hermes passes that JSON to the model as the tool result.

```
Hermes  ──tool call──▶  plugin  ──GET /v1/...──▶  api.autom.dev  ──▶  Google, Bing, Brave…
        ◀──JSON──────          ◀──JSON─────────                 ◀──results page──
```

Results are not cached between calls: two calls with the same query hit the engine twice. To get the next results, call the same tool again with `page` set to 2, 3 and so on.

## Tools

Search tools take a `query`. Optional arguments (country, language, location, page, SafeSearch…) are in each tool's schema, so the model sees them too. Credits are per call.

### Google

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `autom_google_search` | Google web search: organic results (title, link, snippet, position), knowledge graph and pagination. Supports Google operators (site:, intitle:…), country (gl), language (hl), location, time filters (tbs, for example qdr:d for the last day) and SafeSearch. | `query` | 1 |
| `autom_google_search_light` | Fast Google web search that returns organic results only (title, link, snippet, position). Use it when you do not need the knowledge graph or pagination. | `query` | 1 |
| `autom_google_news` | Google News search: articles with title, source, date, snippet and link, by country and language, with pagination. | `query` | 1 |
| `autom_google_images` | Google Images search: images with title, source page, image URL and size. | `query` | 1 |
| `autom_google_videos` | Google Videos search: videos from YouTube and other platforms, with title, channel, duration, date and link. | `query` | 1 |
| `autom_google_shopping` | Google Shopping search: products with title, price, rating, number of ratings, merchant, image and product ID. | `query` | 1 |
| `autom_google_maps` | Google Maps search: places matching a business type, brand or name, with address, website and phone. Use ll (for example @48.8566,2.3522,14z) to search around a point. | `query` | 1 |
| `autom_google_autocomplete` | Google autocomplete suggestions for a query: what people type after it. Useful for keyword research. | `query` | 1 |

### Other search engines

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `autom_search` | Web search with automatic fallback: one call tries Google, then Brave, Bing, DuckDuckGo, Yahoo and Baidu until one answers, and returns its organic results (title, link, snippet, position). Set engines to choose the order. First page only. | `query` | 1 |
| `autom_bing_search` | Bing web search: organic results (title, link, snippet, position), by market (mkt), country (cc), location or GPS coordinates, with pagination. | `query` | 1 |
| `autom_brave_search` | Brave Search web search: organic results (title, link, snippet, position), by country (gl) and language (hl), with pagination. | `query` | 1 |
| `autom_brave_images` | Brave image search: images with title, source page, image URL, thumbnail and size, with SafeSearch and pagination. | `query` | 1 |
| `autom_brave_videos` | Brave video search: videos with title, channel, duration, date, thumbnail and link, with SafeSearch and pagination. | `query` | 1 |
| `autom_duckduckgo_search` | DuckDuckGo web search: organic results (title, link, snippet, position), by country and language, with pagination. | `query` | 1 |
| `autom_yahoo_search` | Yahoo web search: organic results (title, link, snippet, position), by country and language, with pagination. | `query` | 1 |

### Account and helpers

| Tool | What it returns | Input | Credits |
|---|---|---|---|
| `autom_google_locations` | Find the exact location names Google accepts (cities, regions, countries) for the location argument of the Google tools. | `query` | free |
| `autom_usage` | Your Autom account: plan, credits used, credits left, renewal date and rate limit. | none | free |

### Which search tool to use

| Need | Tool |
|---|---|
| A general web search | `autom_google_search` |
| The same, faster and with organic results only | `autom_google_search_light` |
| Results even when an engine is down | `autom_search` (Google, then Brave, Bing, DuckDuckGo, Yahoo, Baidu) |
| A second opinion, or results without Google's ranking | `autom_bing_search`, `autom_brave_search`, `autom_duckduckgo_search`, `autom_yahoo_search` |
| Recent articles on a topic | `autom_google_news`, or `autom_google_search` with `tbs` set to `qdr:d` (last day) or `qdr:w` (last week) |
| Prices and merchants for a product | `autom_google_shopping` |
| Businesses in a place | `autom_google_maps` |
| What people search for around a keyword | `autom_google_autocomplete` |

## Use it as the web_search backend

Hermes's built-in `web_search` tool can also go through Autom. Select it in `hermes tools`, or in `~/.hermes/config.yaml`:

```yaml
web:
  search_backend: autom
```

The backend calls Google Search and returns the organic results (title, link, snippet). It has two settings:

| Setting | Default | Meaning |
|---|---|---|
| `country` | `us` | 2-letter country code the Google results come from, for example `fr` or `de`. |
| `language` | (Google's default) | Interface language, for example `en` or `fr`. |

The backend is search only, so keep an extract backend for `web_extract`. The tools above work with or without this setting.

## Choosing country, language and location

- `gl` is the country of the results (`us`, `fr`, `de`…) and `hl` the language (`en`, `fr`, `de`…). Search results change a lot from one country to another, so set `gl` whenever the question is about a country.
- `google_domain` picks the Google site, for example `google.fr` or `google.co.uk`.
- `location` searches as if from a city or region, for example `Paris, Ile-de-France, France`. Google only accepts its own location names: `autom_google_locations` finds the right one for free.
- `tbs` adds Google's filters, for example `qdr:h` (last hour), `qdr:d` (last day), `qdr:w` (last week), `qdr:m` (last month), `qdr:y` (last year).

## Example prompts

- "Search Google for the best project management tools in 2026 and summarize the top five results."
- "What were the news about OpenAI in the last 24 hours? Use Google News."
- "Find bakeries near the Eiffel Tower on Google Maps and give me their phone numbers."
- "Compare the price of the Sony WH-1000XM5 on Google Shopping in the US and in France."
- "Give me 20 keyword ideas that start with 'web scraping' from Google autocomplete."
- "Search Brave and Bing for 'self-hosted LLM' and tell me which results both engines agree on."
- "Where does example.com rank on Google in Germany for 'cloud hosting'? Check the first three pages."
- "How many Autom credits do I have left?"

## Credits and errors

- Each search uses 1 credit; `autom_google_locations` and `autom_usage` are free. The cost is at the end of each tool's description, so the model knows it before it calls. Plans and prices: [autom.dev/pricing](https://www.autom.dev/pricing).
- Errors come back to the model as `{"error": "Autom: <message>"}` with the API's own message (invalid key, no credits left, bad input), so it can fix the input or try another engine instead of stopping.
- Calls time out after 60 seconds.

## What it does on your machine

- **Network:** calls `https://api.autom.dev` only, with your `AUTOM_API_KEY`. Calls use credits on your Autom account.
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

## Development

```sh
python -m pytest
```

The tests mock the network and run without Hermes installed. `schemas.py` is generated from the Autom OpenAPI spec; each entry holds the tool description, its JSON schema, the API route and the credits per call.

## Contact

- Source: https://github.com/automdev/hermes-plugin-autom
- Autom: https://www.autom.dev
- Issues: https://github.com/automdev/hermes-plugin-autom/issues

## License

MIT
