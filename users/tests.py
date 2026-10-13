import json

from django.test import TestCase

from .models import Subscriber


class ApiSubscribeTests(TestCase):
    url = "/api/subscribe/"

    def post(self, payload, **extra):
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json", **extra
        )

    def test_creates_subscriber(self):
        response = self.post({"email": "a@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], "a@example.com")
        self.assertTrue(Subscriber.objects.filter(email="a@example.com").exists())

    def test_invalid_email(self):
        response = self.post({"email": "not-an-email"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["errors"])

    def test_duplicate_email(self):
        Subscriber.objects.create(email="a@example.com")
        response = self.post({"email": "a@example.com"})
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_cors_header_for_react_dev_server(self):
        response = self.post({"email": "b@example.com"}, HTTP_ORIGIN="http://localhost:5173")
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")
