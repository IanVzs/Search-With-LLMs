<div align="center">
<h1 align="center">Search with LLMs</h1>
Build your own conversational and own llms search engine using this.
<br/>
<a href="https://search.lepton.run/" target="_blank"> fork from lepton </a>
<br/>
<img width="70%" src="https://github.com/leptonai/search_with_lepton/assets/1506722/845d7057-02cd-404e-bbc7-60f4bae89680">
</div>


## Features
- Built-in support for LLM
- Built-in support for search engine
- Customizable pretty UI interface
- Shareable, cached search results

## Setup Search Engine API
There are two default supported search engines: Bing and Google.
 
### Bing Search
To use the Bing Web Search API, please visit [this link](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) to obtain your Bing subscription key.

### Google Search
You have three options for Google Search: you can use the [SearchApi Google Search API](https://www.searchapi.io/) from SearchApi, [Serper Google Search API](https://www.serper.dev) from Serper, or opt for the [Programmable Search Engine](https://developers.google.com/custom-search) provided by Google.

## Makefile

> [!NOTE]
> nodejs npm python

```shell
make build
make run
```


## Build

1. Set Bing subscription key([ ])
```shell
export BING_SEARCH_V7_SUBSCRIPTION_KEY=YOUR_BING_SUBSCRIPTION_KEY
```
2. Build web
```shell
cd web && npm install && npm run build
```
3. Run server
```shell
python main.py
```

For Google Search using SearchApi:
```shell
export SEARCHAPI_API_KEY=YOUR_SEARCHAPI_API_KEY
python main.py
```

For Google Search using Serper:
```shell
export SERPER_SEARCH_API_KEY=YOUR_SERPER_API_KEY
BACKEND=SERPER python main.py
```

For Google Search using Programmable Search Engine:
```shell
export GOOGLE_SEARCH_API_KEY=YOUR_GOOGLE_SEARCH_API_KEY
export GOOGLE_SEARCH_CX=YOUR_GOOGLE_SEARCH_ENGINE_ID
BACKEND=GOOGLE python main
```

