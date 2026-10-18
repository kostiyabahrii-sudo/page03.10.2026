import json

from django.test import TestCase

from .models import Subscriber


class ApiWaitlistTests(TestCase):
    url = "/api/waitlist"

    def post(self, payload, **extra):
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json", **extra
        )

    def test_adds_email(self):
        response = self.post({"email": "a@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "added"})
        self.assertTrue(Subscriber.objects.filter(email="a@example.com").exists())

    def test_existing_email(self):
        Subscriber.objects.create(email="a@example.com")
        response = self.post({"email": "  A@Example.com "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "exists"})
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_invalid_email(self):
        self.assertEqual(self.post({"email": "not-an-email"}).status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(self.url, data="{", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_cors_header_for_react_dev_server(self):
        response = self.post({"email": "b@example.com"}, HTTP_ORIGIN="http://localhost:5173")
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")
