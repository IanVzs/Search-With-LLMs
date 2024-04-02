# -*- coding: utf-8 -*-

import os
import requests
from loguru import logger

from .search_base import SearchBase

'''
This sample makes a call to the Confluence Web UI API with a query and returns relevant web search.
'''

class SearchConfluence(SearchBase):
    # Confluence have Confluence Data Center REST API but i use this web ui api test convenient.
    subscription_key = os.environ.get("CONFLUENCE_COOKIE")
    endpoint = os.environ.get('CONFLUENCE_HOST', "") + "/rest/api/search"
    headers = { 'cookie': subscription_key }

    def search(self, query, mkt='en-US'):
        if not self.alive:
            return None
        params = {
            "cql": f'siteSearch ~ "{query}" AND type in ("space","user","com.atlassian.confluence.extra.team-calendars:calendar-content-type","attachment","page","com.atlassian.confluence.extra.team-calendars:space-calendars-view-content-type","blogpost")',
            "start": 0,
            "limit": 20,
            "excerpt": "highlight",
            "expand": "space.icon",
            "includeArchivedSpaces": False,
            "src": "next.ui.search"
        }
        try:
            # Call the API
            response = requests.get(self.endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            rsp = response.json()
            results = rsp.get("results", [])
            if results:
                for n, v in enumerate(results):
                    results[n]["snippet"] = results[n]["excerpt"].replace("@@@hl", '').replace("@@@", '').replace("endhl", '').replace("h1", '')
                    results[n]["name"] = results[n]["title"].replace("@@@hl", '').replace("@@@", '').replace("endhl", '').replace("h1", '')
                    results[n]["url"] = f"{os.environ['CONFLUENCE_HOST']}{results[n]['url']}"
                return results
            else:
                return "未检索到结果"
        except Exception as ex:
            logger.error(f"Confluence {self.endpoint} error: {ex}")
            raise ex

search_confluence = SearchConfluence()
