from django.test import TestCase
from django.utils import timezone

from .models import Registration, Workshop
from .services import AlreadyRegistered, cancel, register
Status = Registration.Status


class RegisterTests(TestCase):
    def setUp(self):
        self.workshop = Workshop.objects.create(
            title="Test", date=timezone.now(), capacity=2
        )

    def test_first_two_are_confirmed(self):
        a = register(self.workshop.id, "Ali", "ali@test.com")
        b = register(self.workshop.id, "Sara", "sara@test.com")
        self.assertEqual(a.status, Status.CONFIRMED)
        self.assertEqual(b.status, Status.CONFIRMED)

    def test_third_goes_to_waitlist(self):
        register(self.workshop.id, "Ali", "ali@test.com")
        register(self.workshop.id, "Sara", "sara@test.com")
        c = register(self.workshop.id, "Reza", "reza@test.com")
        self.assertEqual(c.status, Status.WAITLIST)

    def test_duplicate_email_is_rejected(self):
        register(self.workshop.id, "Ali", "ali@test.com")
        with self.assertRaises(AlreadyRegistered):
            register(self.workshop.id, "Ali again", "ALI@test.com")


class CancelTests(TestCase):
    def setUp(self):
        self.workshop = Workshop.objects.create(
            title="Test", date=timezone.now(), capacity=1
        )
        self.a = register(self.workshop.id, "Ali", "ali@test.com")
        self.b = register(self.workshop.id, "Sara", "sara@test.com")
        self.c = register(self.workshop.id, "Reza", "reza@test.com")

    def refresh(self):
        for reg in (self.a, self.b, self.c):
            reg.refresh_from_db()

    def test_cancel_confirmed_promotes_first_in_queue(self):
        cancel(self.a.token)
        self.refresh()
        self.assertEqual(self.a.status, Status.CANCELLED)
        self.assertEqual(self.b.status, Status.CONFIRMED)
        self.assertEqual(self.c.status, Status.WAITLIST)

    def test_cancel_waitlisted_changes_nothing_else(self):
        cancel(self.b.token)
        self.refresh()
        self.assertEqual(self.a.status, Status.CONFIRMED)
        self.assertEqual(self.b.status, Status.CANCELLED)
        self.assertEqual(self.c.status, Status.WAITLIST)

    def test_cancelled_user_goes_to_end_of_queue(self):
        cancel(self.b.token)
        register(self.workshop.id, "Sara", "sara@test.com")
        queue = Registration.objects.filter(
            workshop=self.workshop, status=Status.WAITLIST
        ).order_by("created_at", "id")
        self.assertEqual([r.name for r in queue], ["Reza", "Sara"])