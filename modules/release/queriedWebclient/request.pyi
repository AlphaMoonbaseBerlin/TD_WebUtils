"""Info Header Start
Name : request
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End"""
from dataclasses import dataclass
from urllib.parse import urlencode
import json
from cookie import Cookie
from typing import Callable, List
requestCallback = Callable[['Request', 'Response', 'extQueriedWebClient'], None]

@dataclass
class Request:
    method: str
    uri: str
    header: dict
    query: dict
    data: any
    cookies: List[Cookie]

    def __init__(self, server: str, method: str, uri: str='/', query={}, header={}, cookies=[Cookie], data=None, callback=lambda request, response, server: None):
        pass

    def _get_content_type(self):
        pass

    def _get_header(self):
        pass

    def _get_data(self):
        pass

    def _get_method(self):
        pass

    def _get_query(self):
        pass

    def _get_url(self):
        pass