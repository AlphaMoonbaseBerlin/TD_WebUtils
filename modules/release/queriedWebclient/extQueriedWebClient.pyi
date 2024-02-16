"""Info Header Start
Name : extQueriedWebClient
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End"""
import json
from response import Response
from request import Request
import quriedwebclient_exceptions
from cookie import Cookie
from ambMultipart import Multipart
from typing import List, Callable, Dict, Union, Type

def default_callback(request: Request, response: Response, server: COMP):
    pass
requestData = Union[Dict, str, bytes]
requestCallback = Callable[[Request, Response, COMP], None]

class extQueriedWebClient:

    def __init__(self, ownerComp: COMP):
        pass

    @property
    def Server(self):
        pass

    @property
    def _webclient(self) -> webclientDAT:
        pass

    def Timeout(self):
        pass

    def _check_query(self):
        pass

    def _parse_body(self, data):
        pass

    def _read_body(self, data):
        pass

    def _trigger_request(self):
        pass

    def _parse_response(self, status, headerDict, data):
        pass

    def _read_header(self):
        pass

    def QueryRequest(self, requestObject: Request):
        pass

    def Get(self, endpoint: str, params: Dict[str, str]={}, header: Dict[str, str]={}, cookies: list[Cookie]=[], callback: requestCallback=default_callback) -> Request:
        pass

    def Post(self, endpoint: str, params: Dict[str, str]={}, header: Dict[str, str]={}, cookies: list[Cookie]=[], data: requestData=None, callback: requestCallback=default_callback) -> Request:
        method = 'POST'
        pass

    def Put(self, endpoint: str, params: Dict[str, str]={}, header: Dict[str, str]={}, cookies: list[Cookie]=[], data: requestData=None, callback: requestCallback=default_callback) -> Request:
        method = 'PUT'
        pass

    def Patch(self, endpoint: str, params: Dict[str, str]={}, header: Dict[str, str]={}, cookies: list[Cookie]=[], data: requestData=None, callback: requestCallback=default_callback) -> Request:
        method = 'PATCH'
        pass

    def Delete(self, endpoint: str, params: Dict[str, str]={}, header: Dict[str, str]={}, cookies: list[Cookie]=[], data: requestData=None, callback: requestCallback=default_callback) -> Request:
        method = 'DELETE'
        pass

    def Search(self, endpoint: str, params: Dict[str, str]={}, header: Dict[str, str]={}, cookies: list[Cookie]=[], data: requestData=None, callback: requestCallback=default_callback) -> Request:
        method = 'SEARCH'
        pass