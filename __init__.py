from pathlib import Path

from .modules.suspects.project import queriedWebclient as WebclientModules
WebclientComponent = Path(Path(__file__).parent, "modules/release/queriedWebclient.tox").absolute()

from .modules.suspects.project import fileDownloader as FileDownloaderModules
DownloaderComponent = Path(Path(__file__).parent, "modules/release/fileDownloader.tox").absolute()

from .modules.suspects.project import routedWebServer as WebServerModules
WebServerComponent = Path(Path(__file__).parent, "modules/release/routedWebServer.tox").absolute()

    




