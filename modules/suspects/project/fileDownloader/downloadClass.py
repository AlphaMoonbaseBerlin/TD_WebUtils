'''Info Header Start
Name : downloadClass
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 20
Savetimestamp : 2023-08-09T23:26:01.388690
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''

import dataclasses, uuid, typing, td, pathlib, mimetypes, os, datetime
from fileinput import filename
from enum import Enum, auto
from urllib.parse import urlparse

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
    responseHader   : typing.Dict[str, str] = dataclasses.field( default_factory = dict )
    downloaded      : int                   = 0

    requestHeader   : typing.Dict[str, str] = dataclasses.field( default_factory = dict)

    filehandler     : typing.IO[typing.Any] = dataclasses.field( default = None, repr = False)
    filepath        : pathlib.Path          = None
    #filename        : str                  = dataclasses.field( )
    #THis will require some fuckery with getter/setter. Should be possible to automate!
    
    timeout_timer   : td.run                = dataclasses.field( default = None, repr = False)
    meta            : typing.Dict[any,any]  = dataclasses.field( default_factory = dict)

    status          : Status                = Status.IDLE
    timeout_length  : int                   = dataclasses.field( default = 1000, repr = False)

    startTime       : datetime.datetime     = dataclasses.field( default_factory= datetime.datetime.now, repr = False )

    @property
    def size(self):
        return int( self.responseHader.get("content-length", 0) )
    
    @property
    def progress(self):
        return self.downloaded / ( self.size or 1)
    
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
                 startCallback:     typing.Callable,
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
        self.startCallback      = startCallback
        #We are already doing that behaviour in the end, so we actually do not need to do that in the beginning. Not ideal. But with the UUIDs as the proxies
        #we do not know if a file is already in the download queue. 
        #other solution might be do NOT use UUIDs and instead also look for other files with the same stem.
        #But not today!
        #if ExistsBehaviour( self.existsBehaviour ) == ExistsBehaviour.INCREMENT: self.filepath = self._increment( self.filepath )
        if ExistsBehaviour( self.existsBehaviour ) == ExistsBehaviour.KEEP and self.filepath.is_file(): 
            self.start()
            self._done()
    
    def _increment(self, filePath: pathlib.Path):
        index = 0
        stem = filePath.stem
        while filePath.is_file():
            filePath = filePath.with_stem( f"{stem}_{index}")
            index += 1
        return filePath
    
    def _createFilehandler(self):

        if not getattr( self, "started", False): self.startTime = datetime.datetime.now()

        if not self.filepath.suffix:
            self.filepath = self.filepath.with_suffix( mimetypes.guess_extension( self.responseHader.get("content-type", "application/octet-stream") ) )
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
        if self.size <= 0 or self.downloaded < self.size: return
        self._stopTimeout()
        self.filehandler.close()
        self.filepath = self._increment( self.filepath )
        self.download_proxy.rename(
            self.filepath
        )
        self._done()
        

    def update(self, data, header):
        self.status             = Status.RUNNING
        self.responseHader      = header or self.responseHader
        self.filehandler        = self.filehandler or self._createFilehandler()
        self.filehandler.write( data )
        self.downloaded        += len( data )
        self._tick()

    def start(self):
        self.status     = Status.RUNNING
        self.startTime  = datetime.datetime.now()
        self.startet    = True
        self.startCallback( self )
