from pathlib import Path
from .ambMultipart import Multipart
from .cookie import Cookie
from .extQueriedWebClient import extQueriedWebClient
from . import quriedwebclient_exceptions
from .request import Request
from .response import Response

Component = Path(Path(__file__).parent, "modules/release/queriedWebclient.tox").absolute()