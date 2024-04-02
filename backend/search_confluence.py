# -*- coding: utf-8 -*-

import os
import requests
from loguru import logger

'''
This sample makes a call to the Confluence Web UI API with a query and returns relevant web search.
'''

class SearchConfluence:
    # Confluence have Confluence Data Center REST API but i use this web ui api test convenient.
    subscription_key = os.environ["CONFLUENCE_COOKIE"]
    endpoint = os.environ['CONFLUENCE_HOST'] + "/rest/api/search"

    def __init__(self):
        # Construct a request
        self.headers = { 'cookie': SearchConfluence.subscription_key }

    def search(self, query, mkt='en-US'):
        # Call the API
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
            response = requests.get(self.endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            rsp = response.json()
            results = rsp.get("results", [])
            if results:
                for n, v in enumerate(results):
                    results[n]["snippet"] = results[n]["excerpt"]
                    results[n]["name"] = results[n]["title"]
                    results[n]["url"] = f"{os.environ['CONFLUENCE_HOST']}{results[n]['url']}"
                return results
            else:
                return "未检索到结果"
        except Exception as ex:
            logger.error(f"Confluence {self.endpoint} error: {ex}")
            raise ex
