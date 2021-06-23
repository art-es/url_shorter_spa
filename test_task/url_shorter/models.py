from django.conf import settings
from django.db import models
from django.utils import timezone


class ShortenedLink(models.Model):

    original_link = models.TextField()
    subpart = models.CharField(max_length=settings.SUBPART_LENGTH, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    session_id = models.TextField()

    def get_full_link(self):
        return f"{settings.SITE_URL}/{self.subpart}"

    def serialize(self):
        return {
            "original_link": self.original_link,
            "full_link": self.get_full_link(),
        }
