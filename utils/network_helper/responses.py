import json

from rest_framework.response import Response
from middlewares.exceptions import CustomError


class RESPONSES:
    class GENERIC:
        SUCCESS = (101, "Success", 200)
        FAILURE = (102, "Oops, Something went wrong!", 500)
        UNAUTHORIZED = (103, "Unauthorized", 401)
        PERMISSION_DENIED = (105, "Permission Denied", 401)

    class INVALID:
        NETWORK_CALL = (201, "Invalid Request in network call", 500)
        
    class ERRORS:
        class VALIDATIONS:
            MAX_LOGIN_RETRIES   = (405, "Max login attempt exceeded", 400)
            INVALID_STATE       = (406, "State parameter must be an integer.", 400)
            INVALID_ENVIRONMENT = (407, "Environment parameter must be an integer.", 400)
            TOGGLE_DATA_VALIDATION_FAILED = (408, "Toggle data validation failed", 400)

    class FeatureToggle:
        class ERRORS:
            DOES_NOT_EXIST = (801, "Feature toggle does not exist", 400)


def prepare_response(response=RESPONSES.GENERIC.SUCCESS, data=None, extras=None):
    response_payload = {
        "status": response[0],
        "message": response[1],
        "data": data
    }
    if extras:
        response_payload.update(extras)
    return Response(response_payload, status=response[2])


def raise_error(error=None, message=None, status=None):
    if not error:
        error = (0, message, status)
    error = list(error)
    if message:
        error[1] = message
    if status:
        error[2] = status
    raise CustomError({
        "status": error[0],
        "message": error[1],
    }, error[2])
