""" --------------------------------------------------------------------------#
# IMPORTS
# --------------------------------------------------------------------------"""


# Third party dependencies
from flask import request

# Local application dependencies
from config.config import STATUS_ERR


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
