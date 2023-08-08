'''Info Header Start
Name : downloadClass
Author : wieland@MONOMANGO
Version : 0
Build : 18
Savetimestamp : 2023-08-08T16:45:29.059731
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''

import dataclasses, uuid, typing, td, pathlib, mimetypes, os, datetime
from enum import Enum, auto
from urllib.parse import urlparse
import TDFunctions

class Status(Enum):
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()
    DONE = auto()
    INVALID = auto()

class ExistsBehaviour(Enum):
    OVERRIDE    = 0
    KEEP        = 1
    INCREMENT   = 2

@dataclasses.dataclass
class DownloadDataclass:
    source          : str                   = ""
    header          : typing.Dict[str, str] = dataclasses.field( default_factory = dict )
    downloaded      : int                   = 0

    requestHeader   : typing.Dict[str, str] = dataclasses.field( default_factory = dict)

    filehandler     : typing.IO[typing.Any] = None
    filepath        : pathlib.Path          = None

    timeout_timer   : td.run                = None
    meta            : typing.Dict[any,any]  = dataclasses.field( default_factory = dict)

    status          : Status                = Status.IDLE
    timeout_length  : int                   = -1

    startTime       : datetime.datetime     = dataclasses.field( default_factory= datetime.datetime.now )
    @property
    def size(self):
        return int( self.header.get("content-length", 1) )
    
    @property
    def progress(self):
        return self.downloaded / self.size
    
    @property
    def speed(self):
        timedelta = datetime.datetime.now() - self.startTime
        return (self.downloaded / (timedelta.seconds or 1)) or 1

    @property
    def estimatedTime(self):
        return (self.size-self.downloaded) / self.speed
    
class Download ( DownloadDataclass ):
   
    def __init__( self, 
                 source:str, 
                 fileDir:           pathlib.Path, 
                 fileName:          str , 
                 meta:              typing.Dict[any, any], 
                 timeoutLength:     int,
                 existsBehaviour:   ExistsBehaviour, 
                 completeCallback:  typing.Callable, 
                 errorCallback:     typing.Callable,
                 requestHeader:     typing.Dict[str, str] ):
        
        parsedSource    = urlparse( source )
        pathSource      = pathlib.Path( parsedSource.path )
        super().__init__(
            source          = source,
            filepath        = pathlib.Path( fileDir, fileName or pathSource.name ),
            meta            = meta,
            timeout_length  = timeoutLength
        )
        self.requestHeader      = requestHeader
        self.existsBehaviour    = existsBehaviour
        self.completeCallback   = completeCallback
        self.errorCallback      = errorCallback
        
        #We are already doing that behaviour in the end, so we actually do not need to do that in the beginning. Not ideal. But with the UUIDs as the proxies
        #we do not know if a file is already in the download queue. 
        #other solution might be do NOT use UUIDs and instead also look for other files with the same stem.
        #But not today!
        #if ExistsBehaviour( self.existsBehaviour ) == ExistsBehaviour.INCREMENT: self.filepath = self._increment( self.filepath )
        if ExistsBehaviour( self.existsBehaviour ) == ExistsBehaviour.KEEP and self.filepath.is_file(): self._done()
    def _increment(self, filePath: pathlib.Path):
        index = 0
        stem = filePath.stem
        while filePath.is_file():
            filePath = filePath.with_stem( f"{stem}_{index}")
            index += 1
        return filePath
    
    def _createFilehandler(self):
        
        self.startTime = datetime.datetime.now()

        if not self.filepath.suffix:
            self.filepath = self.filepath.with_suffix( mimetypes.guess_extension( self.header.get("content-type", "application/octet-stream") ) )
        if ExistsBehaviour( self.existsBehaviour ) is ExistsBehaviour.OVERRIDE and self.filepath.is_file():
            os.remove( self.filepath )
        self.filepath.parent.mkdir( exist_ok=True, parents=True )
        self.download_proxy = pathlib.Path( self.filepath.parent, str(uuid.uuid4()) )
        return self.download_proxy.open( "wb+" )
    
 

    def _stopTimeout(self):
        try:
            self.timeout_timer.stop()
        except (td.tdError, AttributeError):
            return
        
    def _resetTimeout(self):
        self._stopTimeout()
        self.timeout_timer = run("args[0]()", self._timeout, delayMilliSeconds = self.timeout_length )

    def _done(self):
        self.status = Status.DONE
        self.completeCallback( self )

    def _timeout(self):
        
        self.status = Status.ERROR
        self.download_proxy.close()
        os.remove( self.download_proxy )
        self.errorCallback( self )

    def _tick(self):
        if self.downloaded < self.size: return
        self._stopTimeout()
        self.filehandler.close()
        self.filepath = self._increment( self.filepath )
        self.download_proxy.rename(
            self.filepath
        )
        self._done()
        

    def update(self, data, header):
        self.status             = Status.RUNNING
        self.header             = header or self.header
        self.filehandler        = self.filehandler or self._createFilehandler()
        self.filehandler.write( data )
        self.downloaded        += len( data )
        self._tick()




