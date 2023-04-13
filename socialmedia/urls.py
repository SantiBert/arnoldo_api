from django.urls import include, path

from .views import (
    GetSocialMediaDataView,
    CreateSocialMediaView,
    EditSocialMediaView,
    DeleteSocialMediaView)

urlpatterns = [
    path(
        "all-social-media/",
        GetSocialMediaDataView.as_view(), 
        name="all-social-media"
        ),
    path(
        "social-media/create/",
        CreateSocialMediaView.as_view(), 
        name="create-social-media"
        ),
    path(
        "social-media/<int:social_media_id>/edit/",
        EditSocialMediaView.as_view(), 
        name="edit-social-media"
        ),
    path(
        "social-media/<int:social_media_id>/delete/",
        DeleteSocialMediaView.as_view(), 
        name="delete-social-media"
        ),
    
]