import requests
from rest_framework import generics, status
from rest_framework.response import Response
from CRM.app.users.infrastructure.serializers import UserRegistrationSerializer
from CRM.app.users.domain.factories import UserFactory
from CRM.app.users.domain.models import User
from CRM.app.users.infrastructure.utils import verify_recaptcha


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        recaptcha_response = request.data.get('recaptcha_response')

        # Verify reCAPTCHA response
        if not verify_recaptcha(recaptcha_response):
            return Response({'error': 'reCAPTCHA verification failed'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email address is already in use'}, status=status.HTTP_400_BAD_REQUEST)

        # Use the UserFactory to create the user
        UserFactory.create_user(email=email, username=username, password=password)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
