from django.test import TestCase, override_settings
from fastapi.testclient import TestClient

from config.asgi import get_application


@override_settings(CLOSE_CONNECTIONS_AFTER_REQUEST=True)
class BaseTestCase(TestCase):
    api_client: TestClient

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api_client = TestClient(get_application())


class APITestCase(BaseTestCase):
    def test_retrieving_api_v1_add(self):
        response = self.api_client.get("/api/v1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "world"})
