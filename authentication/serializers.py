from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.http_response_messages import success_messages


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        token = {
            'access_token': data['access'],
            'refresh_token': data['refresh'],
        }

        user = {
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name(),
        }

        response_data = {
            'success': True,
            'data': {'token': token,
                     'user': user, },
            'code': 'access_granted',
            'message': success_messages['access_granted']}

        return response_data
