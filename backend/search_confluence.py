
#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import os 
import requests

'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''

class SearchConfluence:
    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = os.environ["CONFLUENCE_COOKIE"]
    endpoint = os.environ['CONFLUENCE_HOST'] + "/confluence/rest/api/search"

    def __init__(self):
        # Construct a request
        self.headers = { 'cookie': SearchBing.subscription_key }

    def search(self, query, mkt='en-US'):
        # Call the API
        params = { 'q': query, 'mkt': mkt }
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
            raise ex
