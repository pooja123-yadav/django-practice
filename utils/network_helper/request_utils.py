import json

from utils.network_helper.responses import RESPONSES, raise_error


def get_validated_request_body(request):
    try:
        body = request.data
        return body

    except Exception as e:
        raise_error(RESPONSES.INVALID.REQUEST_BODY)
