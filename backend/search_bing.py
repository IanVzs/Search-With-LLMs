
#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import os 
import requests
from loguru import logger

from .search_base import SearchBase

'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''

class SearchBing(SearchBase):
    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = os.environ.get('BING_SEARCH_V7_SUBSCRIPTION_KEY')
    endpoint = os.environ.get('BING_SEARCH_V7_ENDPOINT', "") + "/v7.0/search"

    # Query term(s) to search for. 
    query = "Microsoft"

    # Construct a request
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

    def search(self, query, mkt='en-US'):
        # Call the API
        if not self.alive:
            return None
        params = { 'q': query, 'mkt': mkt }
        try:
            response = requests.get(self.endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            rsp = response.json()
            webPages = rsp.get("webPages")
            if webPages:
                contexts = webPages["value"]
                return contexts
            else:
                return "未检索到结果"
        except Exception as ex:
            raise ex

search_bing = SearchBing()
