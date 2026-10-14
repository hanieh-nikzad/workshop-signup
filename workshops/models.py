import uuid
from django.db import models


class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    admin_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title