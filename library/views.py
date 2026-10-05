from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds the user's name, id and the token lifetime to the login response."""

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = self.user.username
        data['id'] = self.user.id
        minutes = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds() // 60)
        data['token_life_time'] = f'{minutes} minutes'

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
