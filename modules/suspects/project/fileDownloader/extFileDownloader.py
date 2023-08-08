
'''Info Header Start
Name : extFileDownloader
Author : wieland@MONOMANGO
Version : 0
Build : 13
Savetimestamp : 2023-08-08T16:53:59.032337
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''
import os
import downloader_utils
from downloadClass import Download, Status


class extFileDownloader:
	"""
	extFileDownloader description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.log = self.ownerComp.op("logger").Log
		self.query = []
		self.activeDownloads:dict[int,Download] = {}
		self.Query_Download = self.QueryDownload
		self.callback = self.ownerComp.op("callbackManager").Do_Callback

	def QueryDownload(self, sourceUrl, 
		    				targetDir, 
							filename = None, 
							meta = None,
							requestHeader = {} ):
		self.query.append(
			Download(
				source				= sourceUrl, 
				fileDir				= targetDir, 
				fileName			= filename, 
				meta				= meta, 
				timeoutLength		= self.ownerComp.par.Timeout.eval(),
				existsBehaviour 	= self.ownerComp.par.Existsbehaviour.menuIndex,
				completeCallback 	= self._finishDownload,
				errorCallback 		= self._errorDownload,
				requestHeader 		= requestHeader )
		)
		self.log("Querying Download", sourceUrl, targetDir)
		self.checkQuery()
		return

	def checkQuery(self):
		self.log("Checking query.")
		self.log("Items in Query", len(self.query))
		self.log("Active Downloads", len(self.activeDownloads))
		if not self.query: 
			return self.callback("onQueryFinish")
		if len( self.activeDownloads ) >= self.ownerComp.par.Maxparalleldownloads.eval(): return
		self.startDownload( self.query.pop( 0 ) )

	def startDownload(self, download: Download ):
		downloadId = self.ownerComp.op("downloader").request(
			download.source,
			"GET",
			header = download.requestHeader
			#timeout = self.ownerComp.par.Timeout.eval()
		)
		self.log("Starting Download", download)
		self.callback("onDownloadStart", download, self.ownerComp )
		self.activeDownloads[downloadId] = download

	
	def updateDownload(self, id, headerDict, data):
		self.log("Writing Data", id)
		download = self.activeDownloads[id]
		#if download.status != Status.RUNNING: return False
		download.update(data, headerDict)
		self.updateInfo()

	def errorDownload(self, request_id):
		download = self.activeDownloads[request_id]
		self.ownerComp.op("downloader").closeConnection(request_id)
		download._timeout()

	def _clearDownload(self, download:Download, callback_name:str):
		self.callback(callback_name, download, self.ownerComp )

		self.activeDownloads = { key : value for key, value in self.activeDownloads.items() if value != download }
		self.query			= [ value for value in self.query if value != download ]
		self.checkQuery()

	def _errorDownload(self, download):
		self.log("Error Callback")
		self.updateInfo()
		self._clearDownload( download, "onDownloadError" )

	def _finishDownload(self, download):
		self.log("Finish Callback")
		self.updateInfo()
		self._clearDownload( download, "onDownloadFinish" )

	def updateInfo(self):
		statefifo = self.ownerComp.op("state_fifo")
		for key,item in self.activeDownloads.items():
			index = str(key)
			statefifo.row( index ) or statefifo.appendRow( index )
			statefifo.replaceRow( index, [
				index,
				item.source,
				item.status,
				downloader_utils.convert_size(item.size),
				downloader_utils.convert_size(item.downloaded),
				item.progress,
				f"{downloader_utils.convert_size(item.speed)}/s",
				downloader_utils.convert_time( item.estimatedTime ),
				item.filepath,
				item.meta
			])

	