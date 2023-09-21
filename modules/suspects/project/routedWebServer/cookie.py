

'''Info Header Start
Name : cookie
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''
import json
from dataclasses import dataclass

@dataclass
class Cookie:
    key : str
    value : str 
    same_site : str = "Strict"
    max_age : int = 2592000