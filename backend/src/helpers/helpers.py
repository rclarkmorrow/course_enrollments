""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Standard library dependencies.
import json
import requests

# Third party dependencies.
from flask import request

# Local application dependencies.
from config.config import STATUS_ERR, AUTH0


""" --------------------------------------------------------------------------#
# HELPER CLASSES
# --------------------------------------------------------------------------"""


# Raise HTTP status error exceptions
class StatusError(Exception):
    def __init__(self, message, description, status_code):
        self.message = message
        self.description = description
        self.status_code = status_code


""" --------------------------------------------------------------------------#
# HELPER FUNCTIONS
# --------------------------------------------------------------------------"""


# Checks for valid 'details' argument. Returns 'full' by default, errors
# if invalid.
def get_detail():
    detail = request.args.get('detail', None)
    if not detail:
        detail = 'full'
    # Validate argument.
    if detail != 'short' and detail != 'full':
        raise StatusError(
            STATUS_ERR.CODE_422,
            STATUS_ERR.BAD_DETAIL,
            422
        )
    return detail


# Structure CURL request with auth0 configuration and return response with
# bearer tokens for test users.
def get_user_token(test_user):
    url = f'https://{AUTH0.DOMAIN}/oauth/token'
    headers = {"content-type": "application/json"}
    request_data = {
        "client_id": AUTH0.CLIENT_ID,
        "client_secret": AUTH0.CLIENT_SECRET,
        "audience": f'{AUTH0.API_AUDIENCE}',
        "grant_type": "password",
        "username": test_user.NAME,
        "password": test_user.PASSWORD,
        "scope": "openid"
    }
    response = json.loads(requests.post(url, json=request_data,
                                        headers=headers).text)
    return response['access_token']


# Return header with bearer token.
def get_user_token_headers(test_user):
    return {'authorization': "Bearer " + get_user_token(test_user)}
