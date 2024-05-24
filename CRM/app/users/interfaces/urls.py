
from django.urls import path
from CRM.app.users.interfaces.views import UserRegistrationView

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
]
