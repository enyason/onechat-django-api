from django.urls import path

from users.views import UserRegistrationView

urlpatterns = [
    path('users', UserRegistrationView.as_view()),
]
