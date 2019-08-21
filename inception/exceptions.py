from nanohttp import HTTPKnownStatus


class HTTPIncorrectEmailOrPassword(HTTPKnownStatus):
    status = '603 Incorrect Email Or Password'

class HTTPTokenExpired(HTTPKnownStatus):
    status = '609 Token Expired'

class HTTPMalformedAccessToken(HTTPKnownStatus):
    status = '610 Malformed Access Token'

class HTTPMalformedAuthorizationCode(HTTPKnownStatus):
    status = '607 Malformed Authorization Code'

