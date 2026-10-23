from django.db import transaction
from django.utils import timezone

from .models import Registration, Workshop

Status = Registration.Status


class AlreadyRegistered(Exception):
    """این ایمیل قبلاً برای این کارگاه ثبت‌نام کرده است."""


def register(workshop_id, name, email):
    email = email.strip().lower()

    with transaction.atomic():
        workshop = Workshop.objects.select_for_update().get(pk=workshop_id)

        existing = Registration.objects.filter(workshop=workshop, email=email).first()
        if existing and existing.status != Status.CANCELLED:
            raise AlreadyRegistered()

        confirmed_count = workshop.registrations.filter(status=Status.CONFIRMED).count()
        if confirmed_count < workshop.capacity:
            status = Status.CONFIRMED
        else:
            status = Status.WAITLIST

        if existing:
            existing.name = name
            existing.status = status
            existing.created_at = timezone.now()
            existing.save()
            return existing

        return Registration.objects.create(
            workshop=workshop, name=name, email=email, status=status
        )