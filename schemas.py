"""Tool schemas (what the model reads) and how each tool maps to the API.

Each entry: (description, JSON schema of the arguments,
"METHOD /path", {argument: API parameter}, fixed parameters, credits per call, README group).
"""

TOOLS = {
    'autom_google_search': (
        'Google web search: organic results (title, link, snippet, position), knowledge graph and pagination. Supports Google operators (site:, intitle:…), country (gl), language (hl), location, time filters (tbs, for example qdr:d for the last day) and SafeSearch. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Google (supports advanced operators like site:, inurl:, intitle:)."
                },
                "tbs": {
                    "type": "string",
                    "description": "Advanced search filters string (e.g. time ranges: qdr:h last hour, qdr:d last day, qdr:w last week, qdr:m last month, qdr:y last year)."
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. active enables Google SafeSearch; off disables it. Omit to use Google default."
                },
                "location": {
                    "type": "string",
                    "description": "Human-readable location to originate the search from (e.g. New York, NY, Paris, France). If several locations match, the most popular one is used."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                },
                "page": {
                    "type": "number",
                    "description": "Page number / offset used for pagination. Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Maximum number of results to return per page (deprecated). Default: 10."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/search',
        {'query': 'query', 'tbs': 'tbs', 'safe': 'safe', 'location': 'location', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'page': 'page', 'num': 'num'},
        {},
        '1',
        'Google',
    ),
    'autom_google_search_light': (
        'Fast Google web search that returns organic results only (title, link, snippet, position). Use it when you do not need the knowledge graph or pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Google (supports advanced operators like site:, inurl:, intitle:)."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/search/light',
        {'query': 'query', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr'},
        {},
        '1',
        'Google',
    ),
    'autom_google_news': (
        'Google News search: articles with title, source, date, snippet and link, by country and language, with pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query to search on Google News (keywords, company, topic)."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (1 = first page). Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Maximum number of results per page (e.g. 10). Default: 10."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/news',
        {'query': 'query', 'page': 'page', 'num': 'num', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr'},
        {},
        '1',
        'Google',
    ),
    'autom_google_images': (
        'Google Images search: images with title, source page, image URL and size. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query you want to search on Google Images (e.g. \"lion\", \"nike logo\", \"modern house exterior\")."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (1 = first page). Default: 1."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. active enables Google SafeSearch; off disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/images',
        {'query': 'query', 'page': 'page', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'safe': 'safe'},
        {},
        '1',
        'Google',
    ),
    'autom_google_videos': (
        'Google Videos search: videos from YouTube and other platforms, with title, channel, duration, date and link. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Google Videos."
                },
                "location": {
                    "type": "string",
                    "description": "Human-readable location to originate the search from."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (1 = first page). Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Maximum number of results per page (e.g. 10). Default: 10."
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. active enables Google SafeSearch; off disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/videos',
        {'query': 'query', 'location': 'location', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'page': 'page', 'num': 'num', 'safe': 'safe'},
        {},
        '1',
        'Google',
    ),
    'autom_google_shopping': (
        'Google Shopping search: products with title, price, rating, number of ratings, merchant, image and product ID. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query to search on Google Shopping (product name, brand, category)."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (1 = first page). Default: 1."
                },
                "location": {
                    "type": "string",
                    "description": "Location to localize results (e.g. New York, United States). Generates a UULE parameter automatically."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en Default: en."
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                },
                "safe": {
                    "type": "string",
                    "description": "Adult content filter. active enables Google SafeSearch; off disables it. Omit to use Google default."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/shopping',
        {'query': 'query', 'page': 'page', 'location': 'location', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'safe': 'safe'},
        {},
        '1',
        'Google',
    ),
    'autom_google_maps': (
        'Google Maps search: places matching a business type, brand or name, with address, website and phone. Use ll (for example @48.8566,2.3522,14z) to search around a point. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for Google Maps (e.g. business type, brand, or place name)."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (1 = first page). Default: 1."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                },
                "ll": {
                    "type": "string",
                    "description": "Map center / geo hint in Google format (e.g. @43.5131985,1.4600501,60m). Helps focus results around a coordinate and zoom radius."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/maps',
        {'query': 'query', 'page': 'page', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr', 'll': 'll'},
        {},
        '1',
        'Google',
    ),
    'autom_google_autocomplete': (
        'Google autocomplete suggestions for a query: what people type after it. Useful for keyword research. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for which you want to get autocomplete suggestions."
                },
                "google_domain": {
                    "type": "string",
                    "description": "Google domain to use for the search. Defaults to google.com. Examples: - google.com - google.co.uk - google.fr Example: google.com Default: google.com."
                },
                "gl": {
                    "type": "string",
                    "description": "Country to use for the Google search. Two-letter country code (e.g. us for the United States, uk for United Kingdom, or fr for France). Example: us"
                },
                "hl": {
                    "type": "string",
                    "description": "Language to use for the Google search. Two or three-letter language code (e.g. en, es, fr), optionally followed by a region code (e.g. en-gb, es-419). Example: en"
                },
                "cr": {
                    "type": "string",
                    "description": "Limit results to one or more countries. Use country{XX} with | as delimiter (e.g. countryFR|countryDE). Example: countryUS"
                },
                "lr": {
                    "type": "string",
                    "description": "Limit results to one or more languages. Use lang_{xx} with | as delimiter (e.g. lang_fr|lang_de). Example: lang_en"
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/google/search/autocomplete',
        {'query': 'query', 'google_domain': 'google_domain', 'gl': 'gl', 'hl': 'hl', 'cr': 'cr', 'lr': 'lr'},
        {},
        '1',
        'Google',
    ),
    'autom_search': (
        'Web search with automatic fallback: one call tries Google, then Brave, Bing, DuckDuckGo, Yahoo and Baidu until one answers, and returns its organic results (title, link, snippet, position). Set engines to choose the order. First page only. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query."
                },
                "engines": {
                    "type": "string",
                    "description": "Engine order. Default auto tries google, brave, bing, duckduckgo, yahoo, then baidu. A comma-separated list is followed as given. ddg and duck mean duckduckgo. Unknown names are ignored. Default: auto."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code. Defaults to us when omitted. For example us, fr, gb, de."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code. Defaults to en when omitted. For example en, fr, de."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/search',
        {'query': 'query', 'engines': 'engines', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_bing_search': (
        'Bing web search: organic results (title, link, snippet, position), by market (mkt), country (cc), location or GPS coordinates, with pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Bing."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (1 = first page). Default: 1."
                },
                "num": {
                    "type": "number",
                    "description": "Number of results per page (e.g. 10, 20, 50). This value is a suggestion. Default: 10."
                },
                "location": {
                    "type": "string",
                    "description": "Search origin location (e.g. city)."
                },
                "lat": {
                    "type": "number",
                    "description": "GPS latitude for the search origin."
                },
                "lon": {
                    "type": "number",
                    "description": "GPS longitude for the search origin."
                },
                "mkt": {
                    "type": "string",
                    "description": "Market code where results come from (e.g. en-US). Cannot be used together with cc."
                },
                "cc": {
                    "type": "string",
                    "description": "Country code to search from (2-letter ISO 3166-1). Cannot be used together with mkt."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/bing/search',
        {'query': 'query', 'page': 'page', 'num': 'num', 'location': 'location', 'lat': 'lat', 'lon': 'lon', 'mkt': 'mkt', 'cc': 'cc'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_brave_search': (
        'Brave Search web search: organic results (title, link, snippet, position), by country (gl) and language (hl), with pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Brave Search."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code, for example us, fr, gb, de. Default: us."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code, for example en, fr, de. Default: en."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/brave/search',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_brave_images': (
        'Brave image search: images with title, source page, image URL, thumbnail and size, with SafeSearch and pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Brave Images."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination (50 results per page). Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code (e.g. fr, us). Mapped to Brave country."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code (e.g. fr, en). Mapped to Brave lang."
                },
                "safe": {
                    "type": "string",
                    "description": "SafeSearch: active | off | moderate | strict. Google-style active maps to Brave strict."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/brave/images',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl', 'safe': 'safe'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_brave_videos': (
        'Brave video search: videos with title, channel, duration, date, thumbnail and link, with SafeSearch and pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to run on Brave Videos."
                },
                "page": {
                    "type": "number",
                    "description": "Page number for pagination. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code (e.g. fr, us). Mapped to Brave country."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code (e.g. fr, en). Mapped to Brave lang."
                },
                "safe": {
                    "type": "string",
                    "description": "SafeSearch: active | off | moderate | strict. Google-style active maps to Brave strict."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/brave/videos',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl', 'safe': 'safe'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_duckduckgo_search': (
        'DuckDuckGo web search: organic results (title, link, snippet, position), by country and language, with pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query sent to DuckDuckGo Search."
                },
                "page": {
                    "type": "number",
                    "description": "Page number. Page 1 is the first page of results. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code, for example us, fr, gb, de, jp."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code, for example en, fr, de, ja, zh."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/duckduckgo/search',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_yahoo_search': (
        'Yahoo web search: organic results (title, link, snippet, position), by country and language, with pagination. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query sent to Yahoo Search."
                },
                "page": {
                    "type": "number",
                    "description": "Page number. Page 1 is the first page of results. Default: 1."
                },
                "gl": {
                    "type": "string",
                    "description": "Country code, for example us, fr, gb, de, jp."
                },
                "hl": {
                    "type": "string",
                    "description": "Language code, for example en, fr, de, ja, zh."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/yahoo/search',
        {'query': 'query', 'page': 'page', 'gl': 'gl', 'hl': 'hl'},
        {},
        '1',
        'Other search engines',
    ),
    'autom_google_locations': (
        'Find the exact location names Google accepts (cities, regions, countries) for the location argument of the Google tools. Free.',
        {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search locations supported by Piloterr (cities, countries, etc.) by providing a query string. Returns matching locations ordered by reach."
                }
            },
            "required": [
                "query"
            ]
        },
        'GET /v1/finder/google-locations',
        {'query': 'query'},
        {},
        None,
        'Account and helpers',
    ),
    'autom_usage': (
        'Your Autom account: plan, credits used, credits left, renewal date and rate limit. Free.',
        {
            "type": "object",
            "properties": {},
            "required": []
        },
        'GET /v1/usage',
        {},
        {},
        None,
        'Account and helpers',
    ),
}
