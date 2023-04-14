import pytest

from rest_framework.test import APIClient

from socialmedia.models import SocialMedia, EnlaceSocial

from django.urls import reverse

from users.test.fixtures import common_user_token

@pytest.mark.django_db()
def test_get_social_media_list_successfully():
    client = APIClient()
    social_media = SocialMedia.objects.create(
        name = 'Instagram'
    )
    link = EnlaceSocial.objects.create(
        social_media = social_media,
        link = 'https://www.instagram.com/'
    )
    url = reverse("all-social-media")
    response = client.get(url)
    assert response.status_code == 200
    data = response.json().get("social_media")
    assert len(data) == 1
    
@pytest.mark.django_db()
def test_create_social_media_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    payload = {
        "name": "Instagram",
        "icon": "fa Instagram",
        "link": "https://www.instagram.com/",
        }
    url = reverse("create-social-media")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 200
    
@pytest.mark.django_db()
def test_create_social_media_bad_request(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    payload = {
        "name": None,
        "icon": "fa Instagram",
        "link": "https://www.instagram.com/",
        }
    url = reverse("create-social-media")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 400

@pytest.mark.django_db()
def test_create_social_anonnymus_user():
    client = APIClient()
    payload = {
        "name": "Instagram",
        "icon": "fa Instagram",
        "link": "https://www.instagram.com/",
        }
    url = reverse("create-social-media")
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 401

@pytest.mark.django_db()
def test_edit_social_media_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    
    social_media = SocialMedia.objects.create(
        name = 'Facebook'
    )
    link = EnlaceSocial.objects.create(
        social_media = social_media,
        link = 'https://www.facebook.com/'
    )
    
    payload = {
        "name": "Instagram",
        "icon": "fa Instagram",
        "link": "https://www.instagram.com/",
        }
    url = reverse("edit-social-media",kwargs={"social_media_id": social_media.id})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 200

@pytest.mark.django_db()
def test_edit_social_media_not_exists(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    
    social_media = SocialMedia.objects.create(
        name = 'Facebook'
    )
    link = EnlaceSocial.objects.create(
        social_media = social_media,
        link = 'https://www.facebook.com/'
    )
    
    payload = {
        "name": "Instagram",
        "icon": "fa Instagram",
        "link": "https://www.instagram.com/",
        }
    url = reverse("edit-social-media",kwargs={"social_media_id":999})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 404
    data = response.json().get("error")
    assert data == "Social media does not exist"


@pytest.mark.django_db()
def test_edit_social_media_bad_request(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    
    social_media = SocialMedia.objects.create(
        name = 'Facebook'
    )
    link = EnlaceSocial.objects.create(
        social_media = social_media,
        link = 'https://www.facebook.com/'
    )
    
    payload = {
        "name": "Instagram",
        "icon": "fa Instagram",
        "link": 9999,
        }
    url = reverse("edit-social-media",kwargs={"social_media_id":social_media.id})
    response = client.post(
        url,
        data=payload,
        format="json",
    )
    assert response.status_code == 400
    
@pytest.mark.django_db()
def test_delete_social_media_successfully(common_user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + common_user_token)
    
    social_media = SocialMedia.objects.create(
        name = 'Facebook'
    )
    link = EnlaceSocial.objects.create(
        social_media = social_media,
        link = 'https://www.facebook.com/'
    )
    
    url = reverse("delete-social-media",kwargs={"social_media_id": social_media.id})
    response = client.delete(url)
    assert response.status_code == 200
    data = response.json().get("message")
    assert data == "Social media deleted"
    result_media = SocialMedia.objects.filter(id=social_media.id).exists()
    assert result_media == False
    
    