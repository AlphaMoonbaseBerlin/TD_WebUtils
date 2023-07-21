
'''Info Header Start
Name : request
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 4
Savetimestamp : 2023-07-21T11:11:22.164611
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''
import json
from dataclasses import dataclass

@dataclass
class Request:
	method : str
	header : dict
	uri    : str
	params : dict
	query  : dict
	data   : any
	cookies : dict
	_td_request : any

	def __init__(self, td_request:dict):
		self._td_request = td_request
		self.method:str 	= td_request["method"]
		self.header:dict 	= Request._parse_header(td_request)
		self.uri:str 		= td_request["uri"]
		self.cookies:dict	= Request._parse_cookies( td_request.get("Cookie", "") )
		self.query:dict 	= td_request["pars"]
		self.data:any 		= Request._try_parse_data( td_request["data"] )
		self.params:dict 	= {}
	
	@staticmethod
	def _parse_cookies(cookiestring:str):
		cookiestrings = cookiestring.split(";")
		return_dict = {}
		for key_value_string in cookiestrings:
			if not key_value_string: continue
			key, value = key_value_string.split("=")
			return_dict[key] = value
		return return_dict

	@staticmethod
	def _parse_header( td_dict:dict ):
		#Header Values get added to the default TD-Dict directly, not a seperate header.
		#THis means we have to filter the default entries out by hand. 
		#Bad decission tbh
		#To be in line with the rest of TD we will lowercase the entries.
		default_entries = ['method','uri','pars','clientAddress','serverAddress','data']
		return {
			key.lower() : value for key,value in td_dict.items() if key not in default_entries
		}

	@staticmethod
	def _try_parse_data(data):
		try:
			return json.loads( data )
		except:
			return data


