
'''Info Header Start
Name : cookie
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 3
Savetimestamp : 2023-07-19T21:23:38.937945
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import json
from dataclasses import dataclass

@dataclass
class Cookie:
    key : str
    value : str 
    same_site : str = "Strict"
    max_age : int = 2592000