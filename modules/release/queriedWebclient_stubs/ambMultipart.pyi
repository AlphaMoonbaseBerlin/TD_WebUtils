"""Info Header Start
Name : ambMultipart
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End"""
import mimetypes
from io import BytesIO
from pathlib import Path
strCodec = 'ISO-8859-1'

class Multipart:

    def __init__(self) -> None:
        pass

    def AddField(self, name: str, value: any):
        pass

    def AddFile(self, name: str, filepath: Path):
        pass

    def boundaryPart(self, prefix='', suffix=''):
        pass

    def Parse(self):
        pass