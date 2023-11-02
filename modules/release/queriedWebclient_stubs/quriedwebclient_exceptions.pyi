"""Info Header Start
Name : quriedwebclient_exceptions
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End"""

class WebClientError(Exception):
    pass

class UserError(WebClientError):
    pass

class BadRequest(UserError):
    pass

class Unauthorized(UserError):
    pass

class Forbidden(UserError):
    pass

class NotFound(UserError):
    pass

class MethodNotAllowed(UserError):
    pass

class Timeout(UserError):
    pass

class Gone(UserError):
    pass

class ServerError(WebClientError):
    pass

class InternalServerError(ServerError):
    pass

class NotImplemented(ServerError):
    pass

class BadGateway(ServerError):
    pass

class ServiceUnavailable(ServerError):
    pass

class GatewayTimeout(ServerError):
    pass
exception_dict = {400: BadRequest, 401: Unauthorized, 403: Forbidden, 404: NotFound, 405: MethodNotAllowed, 410: Gone, 500: InternalServerError, 501: NotImplemented, 502: BadGateway, 503: ServiceUnavailable, 504: GatewayTimeout}

def get_default(code):
    pass

def get(code):
    pass