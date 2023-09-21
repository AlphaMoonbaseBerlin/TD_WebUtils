
'''Info Header Start
Name : exceptions
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''
class WebClientError(Exception):
    pass

class UserError(WebClientError):
    pass

#200
class OK(WebClientError):
	pass

#400
class BadRequest(UserError):
    pass

#401
class Unauthorized(UserError):
    pass

#403
class Forbidden(UserError):
    pass

#404
class NotFound(UserError):
    pass

#405 
class MethodNotAllowed(UserError):
    pass
    
class Timeout(UserError):
	pass
#410
class Gone(UserError):
    pass

###
class ServerError(WebClientError):
    pass

#500
class InternalServerError(ServerError):
    pass

#501
class NotImplemented(ServerError):
    pass

#502
class BadGateway(ServerError):
    pass

#503
class ServiceUnavailable(ServerError):
    pass

#504
class GatewayTimeout(ServerError):
    pass


exception_dict = {
	OK				: 200,
    BadRequest 		: 400,
    Unauthorized 	: 401,
    Forbidden		: 403,
    NotFound		: 404,
    MethodNotAllowed: 405,
    Gone 			: 410,
    InternalServerError : 500,
    NotImplemented 	: 501,
    BadGateway		: 502,
    ServiceUnavailable : 503,
    GatewayTimeout : 504
}
def get_default( code ):
    if 400 <= code <= 499: return UserError
    if 500 <= code <= 599: return ServerError
    return None

def get( code ):
    return exception_dict.get( code, get_default(code) )