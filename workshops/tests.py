from django.test import TestCase
from django.utils import timezone

from .models import Registration, Workshop
from .services import AlreadyRegistered, register

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