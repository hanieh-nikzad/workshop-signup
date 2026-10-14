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


class Registration(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "تأییدشده"
        WAITLIST = "waitlist", "لیست انتظار"
        CANCELLED = "cancelled", "لغوشده"

    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="registrations"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.WAITLIST
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["workshop", "email"],
                name="unique_email_per_workshop",
            )
        ]

    def str(self):
        return f"{self.name} ({self.status})"