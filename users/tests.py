import json
from unittest import mock

from django.core import signing
from django.test import TestCase

from .models import Subscriber
from .views import SURVEY_SALT


class ApiWaitlistTests(TestCase):
    url = "/api/waitlist"

    def post(self, payload, **extra):
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json", **extra
        )

    def test_adds_email(self):
        response = self.post({"email": "a@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "added")
        subscriber = Subscriber.objects.get(email="a@example.com")
        # Until the survey is answered, the person is stored as "none".
        self.assertEqual(subscriber.heard_from, Subscriber.Source.NONE)
        self.assertEqual(subscriber.heard_from_other, "")

    def test_existing_email(self):
        Subscriber.objects.create(email="a@example.com")
        response = self.post({"email": "  A@Example.com "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "exists")
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_invalid_email(self):
        self.assertEqual(self.post({"email": "not-an-email"}).status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(self.url, data="{", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_json_that_is_not_an_object(self):
        for body in ("[]", '"a@example.com"', "null", "1"):
            response = self.client.post(
                self.url, data=body, content_type="application/json"
            )
            self.assertEqual(response.status_code, 400, body)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_cors_header_for_react_dev_server(self):
        response = self.post({"email": "b@example.com"}, HTTP_ORIGIN="http://localhost:5173")
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")

    def test_survey_token_offered_to_new_email(self):
        token = self.post({"email": "a@example.com"}).json()["survey_token"]
        subscriber = Subscriber.objects.get(email="a@example.com")
        self.assertEqual(signing.loads(token, salt=SURVEY_SALT), subscriber.pk)

    def test_survey_token_offered_again_while_unanswered(self):
        Subscriber.objects.create(email="a@example.com")
        self.assertIsNotNone(self.post({"email": "a@example.com"}).json()["survey_token"])

    def test_no_survey_token_once_answered(self):
        Subscriber.objects.create(email="a@example.com", heard_from="friend")
        self.assertIsNone(self.post({"email": "a@example.com"}).json()["survey_token"])


class ApiWaitlistSourceTests(TestCase):
    url = "/api/waitlist/source"

    def setUp(self):
        self.subscriber = Subscriber.objects.create(email="a@example.com")
        self.token = signing.dumps(self.subscriber.pk, salt=SURVEY_SALT)

    def post(self, payload):
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

    def answer(self, **payload):
        return self.post({"token": self.token, **payload})

    def stored(self):
        self.subscriber.refresh_from_db()
        return self.subscriber.heard_from, self.subscriber.heard_from_other

    def test_saves_fixed_options(self):
        for source in ("friend", "social", "ai"):
            response = self.answer(source=source)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "saved"})
            self.assertEqual(self.stored(), (source, ""))

    def test_saves_other_with_text(self):
        self.assertEqual(
            self.answer(source="other", other="  a podcast ").status_code, 200
        )
        self.assertEqual(self.stored(), ("other", "a podcast"))

    def test_other_text_is_truncated(self):
        self.answer(source="other", other="x" * 500)
        self.assertEqual(len(self.stored()[1]), 200)

    def test_other_text_ignored_for_fixed_options(self):
        self.answer(source="friend", other="should not be stored")
        self.assertEqual(self.stored(), ("friend", ""))

    def test_other_without_text_is_allowed(self):
        self.assertEqual(self.answer(source="other").status_code, 200)
        self.assertEqual(self.stored(), ("other", ""))

    def test_rejects_unknown_source_and_none(self):
        for source in ("none", "nope", "", None, 1, ["friend"]):
            self.assertEqual(self.answer(source=source).status_code, 400, source)
        self.assertEqual(self.stored(), ("none", ""))

    def test_rejects_bad_token(self):
        for token in ("", "garbage", None, 5):
            response = self.post({"token": token, "source": "friend"})
            self.assertEqual(response.status_code, 400, token)
        # A token signed with a different salt must not work either.
        forged = signing.dumps(self.subscriber.pk, salt="something-else")
        self.assertEqual(
            self.post({"token": forged, "source": "friend"}).status_code, 400
        )
        self.assertEqual(self.stored(), ("none", ""))

    def test_rejects_expired_token(self):
        with mock.patch("users.views.SURVEY_MAX_AGE", -1):
            response = self.answer(source="friend")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.stored(), ("none", ""))

    def test_unknown_subscriber(self):
        self.subscriber.delete()
        self.assertEqual(self.answer(source="friend").status_code, 404)

    def test_invalid_json(self):
        response = self.client.post(self.url, data="{", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_cors_header_for_react_dev_server(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"token": self.token, "source": "friend"}),
            content_type="application/json",
            HTTP_ORIGIN="http://localhost:5173",
        )
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")
