from django.db import models
from django.utils import timezone

class Season(models.Model):
    name = models.CharField(max_length=150)
    image = models.CharField(max_length=600, null=True, blank=True)
    banner =  models.CharField(max_length=600, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Episodies(models.Model):
    name = models.CharField(max_length=150)
    season = models.ForeignKey(
        Season, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    link1 = models.URLField('Link 1', max_length=1300, null=True, blank=True)
    link2 = models.URLField('Link 2', max_length=1300, null=True, blank=True)
    english = models.URLField(
        'English', max_length=1300, null=True, blank=True)
    spoty = models.URLField('Spotify', max_length=1300, null=True, blank=True)
    mediafire = models.URLField(
        'Mediafire', max_length=1300, null=True, blank=True)
    original_name = models.CharField(max_length=150,null=True, blank=True)
    original_date = date = models.DateField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class EpisodiePicture(models.Model):
    episodie = models.ForeignKey(
        Episodies, on_delete=models.PROTECT, related_name="pictures"
    )
    picture = models.CharField(max_length=600)
    is_default = models.BooleanField(default=True)