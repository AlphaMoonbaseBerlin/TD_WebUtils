'''Info Header Start
Name : cookie
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 4
Savetimestamp : 2023-07-21T15:32:36.279050
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''
import datetime
import json
from dataclasses import dataclass

@dataclass
class Cookie:
    key         : str
    value       : str 
    settings    : dict

    def __init__(self, cookie_string:str):
        self.settings = {}
        for index,element in enumerate ( cookie_string.split(";") ):
            elements = element.split("=")
            if not index:  
                key, value = elements
                self.key = key
                self.value = value
                continue
            
            if len( elements ) == 1: self.settings[elements[0]] = True
            elif len( elements ) == 2: 
                key, value = elements
                self.settings[key] = value
            

            
            