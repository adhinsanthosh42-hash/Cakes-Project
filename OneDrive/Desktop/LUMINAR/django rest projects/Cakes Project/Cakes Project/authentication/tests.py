import smtplib
from unittest.mock import patch

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from .models import profile
from .serializers import ProfileSerializer


class ProfileAdminTests(SimpleTestCase):
    def test_profile_string_representation_uses_username(self):
        user = profile(username="adhinsanthosh")

        self.assertEqual(str(user), "adhinsanthosh")

    def test_profiles_are_registered_with_role_visible(self):
        profile_admin = admin.site._registry[profile]

        self.assertIsInstance(profile_admin, UserAdmin)
        self.assertIn("role", profile_admin.list_display)
        self.assertIn("password", profile_admin.fieldsets[0][1]["fields"])
        self.assertTrue(
            any("last_login" in fieldset[1].get("fields", ()) for fieldset in profile_admin.fieldsets)
        )
        self.assertTrue(
            any("role" in fieldset[1].get("fields", ()) for fieldset in profile_admin.fieldsets)
        )


class RegistrationTests(TestCase):
    def test_serializer_hashes_the_submitted_password_and_saves_email(self):
        serializer = ProfileSerializer(
            data={
                "username": "cake@example.com",
                "password": "a-strong-password",
                "role": "user",
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save(email=serializer.validated_data["username"])

        self.assertTrue(user.check_password("a-strong-password"))
        self.assertEqual(user.email, "cake@example.com")

    @patch(
        "authentication.views.send_mail",
        side_effect=smtplib.SMTPServerDisconnected("connection unexpectedly closed"),
    )
    def test_email_failure_does_not_turn_successful_registration_into_server_error(
        self, send_mail_mock
    ):
        response = APIClient().post(
            "/register/",
            {
                "username": "cake@example.com",
                "password": "a-strong-password",
                "role": "user",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("email could not be sent", response.data["msg"])
        self.assertTrue(profile.objects.get(username="cake@example.com").check_password(
            "a-strong-password"
        ))
        send_mail_mock.assert_called_once()
