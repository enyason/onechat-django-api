import rest_framework
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from common.http_response_utils import http_error_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        return http_error_response(f"{exc.default_detail}",
                                   {'response_code': exc.default_code},
                                   http_status=response.status_code)

    try:
        print(f"Error :{response}")
        print(f"Error :{type(exc)}")
        if response:
            return http_error_response(f"{response.data}",
                                       {'response_code': "request_failed"},
                                       http_status=response.status_code)
        else:
            return http_error_response(f"{str(exc)}",
                                       {'response_code': "request_failed"},
                                       http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception:
        return http_error_response("Can not process this request,kindly contact dev support.",
                                   {'response_code': "request_failed"},
                                   http_status=response.status_code)
