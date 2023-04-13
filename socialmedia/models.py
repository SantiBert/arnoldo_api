from django.db import models

class SocialMedia(models.Model):
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=600, null=True, blank=True)

    def __str__(self):
        return self.name

class EnlaceSocial(models.Model):
    social_media = models.ForeignKey(
        SocialMedia, on_delete=models.PROTECT, related_name="links"
    )
    link = models.URLField()