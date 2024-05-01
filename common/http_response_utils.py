from typing import Any
from rest_framework import status
from rest_framework.response import Response


def http_success_response(message: str,
                          code: str,
                          data: Any = None,
                          http_status: int = status.HTTP_200_OK) -> Response:
    return Response({
        'success': True,
        'data': data,
        'message': message,
        'code': code
    }, status=http_status)


def http_error_response(message: str, code: str, data: Any = None,
                        http_status: int = status.HTTP_400_BAD_REQUEST) -> Response:
    return Response({
        'success': False,
        'data': data,
        'message': message,
        'code': code
    }, status=http_status)
