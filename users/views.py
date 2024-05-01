from django.core.validators import validate_email
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.http_response_messages import error_messages, success_messages
from common.http_response_utils import http_error_response, http_success_response
from users.models import User


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        email: str = request.data.get('email')
        username: str = request.data.get('username')
        password: str = request.data.get('password')
        full_name: str = request.data.get('full_name')

        # Validate input data
        if not email or not password or not full_name or not username:
            return http_error_response(error_messages['invalid_user_details'],
                                       code='invalid_user_details',
                                       data=None,
                                       http_status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return http_error_response(error_messages['invalid_email'],
                                       code='invalid_email',
                                       http_status=status.HTTP_400_BAD_REQUEST)

            # Check if user with given username already exists
        try:
            existing_user = User.objects.get(username=username)
            return http_error_response(error_messages['user_name_already_taken'],
                                       code='user_name_already_taken',
                                       http_status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

            # Check if user with given email already exists
        try:
            existing_user = User.objects.get(email=email)
            return http_error_response(error_messages['email_already_exists'],
                                       code='email_already_exists',
                                       http_status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

            # Split full_name into first_name and last_name
        names: list[str] = full_name.split(' ')
        first_name: str = names[0]
        last_name: str = ' '.join(names[1:]) if len(names) > 1 else ''

        # Create user
        User.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return http_success_response(message=success_messages['successful_user_registration'],
                                     code='successful_user_registration',
                                     http_status=status.HTTP_201_CREATED)
