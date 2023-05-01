# -*- coding: utf-8 -*-
import json
import unittest

from fastapi.testclient import TestClient
from unittest.mock import patch
from service.api.health import HealthCheckResponseModel
from service.main import app

client = TestClient(app)


class TestHealthMain(unittest.TestCase):
    def test_health_main(self):
        response = client.get("/api/health/status")

        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        response_model = HealthCheckResponseModel(**response_dict)

        self.assertEqual(response_model.status, "up")
        self.assertEqual(response.status_code, 200)


class TestSystemInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_system_info(self) -> None:
        response = self.client.get("/api/health/system-info")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("current_datetime", data)
        self.assertIsInstance(data["current_datetime"], str)

        self.assertIn("cpu_info", data)


class TestProcesses(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_processes(self):
        response = self.client.get("/api/health/processes")

        # check if response status code is 200
        self.assertEqual(response.status_code, 200)

        # assert that response contains 'current_datetime' and 'running_processes' keys
        response_data = response.json()
        self.assertIn("current_datetime", response_data)
        self.assertIn("running_processes", response_data)


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app=app)

    def test_successful_request_returns_json(self):
        response = self.client.get("/api/health/configuration")

        # Assert that the response is successful and has content-type application/json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

        # Attempt to parse the response as JSON and assert it's a dictionary
        try:
            configuration_data = json.loads(response.content)
            self.assertIsInstance(configuration_data, dict)
        except ValueError:
            self.fail("Response was not valid JSON")


class TestHeapDumpEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_heapdump(self):
        response = self.client.get("api/health/heapdump")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain; charset=utf-8")


class TestHealthDatabase(unittest.TestCase):
    async def test_success(self):
        # Test a successful database connection
        response = client.get("/api/health/database")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(
        #     response.json(),
        #     {"database": "up", "database_type": "PostgreSQL", "version": "10.0"},
        # )

    async def test_failure(self):
        # Test a failed database connection
        # First, we need to mock the db.execute method to raise an exception
        with patch(
            "service.database.db_session.AsyncDatabaseSession._session.execute"
        ) as mock_execute:
            mock_execute.side_effect = Exception("Connection failed")
            response = await client.get("/api/health/database")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {"database": "down", "error_message": "Connection failed"},
            )


# if __name__ == "__main__":
#     unittest.main()
