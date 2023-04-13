import pytest
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
@pytest.fixture
def common_user_token():
    user = User.objects.create_user(username='testuser', password='testpass')
    token = Token.objects.create(user=user)
    return token.key