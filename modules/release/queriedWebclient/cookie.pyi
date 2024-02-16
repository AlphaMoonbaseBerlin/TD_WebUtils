"""Info Header Start
Name : cookie
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End"""
import datetime
import json
from dataclasses import dataclass

@dataclass
class Cookie:
    key: str
    value: str
    settings: dict

    def __init__(self, cookie_string: str):
        pass