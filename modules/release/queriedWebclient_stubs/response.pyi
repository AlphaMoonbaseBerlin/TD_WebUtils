"""Info Header Start
Name : response
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End"""
import json
from dataclasses import dataclass
from cookie import Cookie

@dataclass
class Response:
    statuscode: int
    statusreason: str
    header: dict
    cookies: list
    data: any
    raw_data: any

    def __init__(self, statuscode, statusreason, header_dict, raw_response):
        pass

    @staticmethod
    def _parse_response(raw_data):
        pass