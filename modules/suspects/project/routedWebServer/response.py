
'''Info Header Start
Name : response
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 3
Savetimestamp : 2023-07-19T21:23:41.745068
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import json
from dataclasses import dataclass

@dataclass
class Response:
    statuscode : int
    statusreason : str
    header : dict
    cookies : list
    data : any
    _td_response : any

    def __init__(self, td_response):
        self._td_response = td_response
        self.statuscode = 404
        self.statusreason = "Unhandles Response"
        self.header = {}
        self.cookies = []
        self.data = None

    def _parse_header(self):
        for key, value in self.header.items():
            self._td_response[ key ] = value
    
    def _parse_cookies(self):
        cookie_string = "\nSet-Cookie: ".join( [ f"{cookie.key}={cookie.value};SameSite={cookie.same_site};Max-Age={cookie.max_age};" for cookie in self.cookies] )
        if cookie_string:
            
            #cookie_string += "\n" * bool( cookie_string )
            self._td_response["Set-Cookie"] = cookie_string

    def _parse_data(self):
        if isinstance( self.data, str): self.data = self.data.encode()
        try:
            self._td_response["data"] = json.dumps( self.data )
            self.header["Content-Type"] = "application/json"
        except:
            self._td_response["data"] = self.data

    def _parse_status(self):
        self._td_response["statusCode"] = self.statuscode
        self._td_response["statusReason"] = self.statusreason

    def _parsed_response(self):
        self._parse_header()
        self._parse_data()
        self._parse_status()
        self._parse_cookies()
        return self._td_response