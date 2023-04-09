import unittest
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from src.service.api.health import HealthCheckResponseModel
from src.service.main import app

client = TestClient(app)


class TestHealthMain(unittest.TestCase):
    def test_health_main(self):
        response = client.get("/api/health/status")

        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        response_model = HealthCheckResponseModel(**response_dict)

        self.assertEqual(response_model.status, "UP")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
