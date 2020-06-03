""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from config.config import AUTH0, STATUS_ERR
from helpers.helpers import StatusError


""" --------------------------------------------------------------------------#
# AUTH HEADER
# --------------------------------------------------------------------------"""


# Gets the authorization header and validates it.
def get_token_auth_header():
    # Gets header.
    auth_header = request.headers.get("Authorization", None)
    # Checks for an Authorization header.
    if not auth_header:
        raise StatusError(STATUS_ERR.CODE_401,
                          STATUS_ERR.HEADER_MISSING, 401)

    # Heater parts to list
    auth_header_parts = auth_header.split()

    # Checks that header starts with Bearer.
    if auth_header_parts[0].lower() != 'bearer':
        raise StatusError(STATUS_ERR.CODE_401,
                          STATUS_ERR.BEARER_MISSING, 401)
    # Checks for inclusion of token.
    elif len(auth_header_parts) == 1:
        raise StatusError(STATUS_ERR.CODE_401,
                          STATUS_ERR.TOKEN_MISSING, 401)
    elif len(auth_header_parts) > 2:
        raise StatusError(STATUS_ERR.CODE_401,
                          STATUS_ERR.BEARER_TOKEN, 401)

    # Get token from header and return.
    return auth_header_parts[1]


# Checks that permissions are included in the payload.
def check_permissions(permission, payload):
    # Check payload for permissions.
    if 'permissions' in payload:
        # Check that required permission is in permissions.
        if permission not in payload['permissions']:
            raise StatusError(STATUS_ERR.CODE_401,
                              STATUS_ERR.NOT_AUTHORIZED, 401)
    else:
        raise StatusError(STATUS_ERR.CODE_401,
                          STATUS_ERR.PERMISSIONS_MISSING, 400)

    return True


# Verifies authorization token, and returns payload
def verify_decode_jwt(token):
    # Get the public key from Auth0.com
    jsonurl = urlopen('https://'+AUTH0.DOMAIN+'/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # Get the token from the header.
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    # Converts public keys to dict.
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Verify the token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=AUTH0.ALGORITHMS,
                audience=AUTH0.API_AUDIENCE,
                issuer='https://'+AUTH0.DOMAIN+'/'
            )
        except jwt.ExpiredSignatureError:
            raise StatusError(STATUS_ERR.CODE_401,
                              STATUS_ERR.TOKEN_EXPIRED, 401)
        except jwt.JWTClaimsError:
            raise StatusError(STATUS_ERR.CODE_401,
                              STATUS_ERR.INV_CLAIMS, 401)
        except Exception:
            raise StatusError(STATUS_ERR.CODE_400,
                              STATUS_ERR.PARSE_TOKEN, 400)
        _request_ctx_stack.top.current_user = payload
        return payload

    raise StatusError(STATUS_ERR.CODE_401,
                      STATUS_ERR.KEY_FIND, 401)


# Decorator for methods that require authorization and
# specific permissions.
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
