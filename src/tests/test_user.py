import json
from unittest import TestCase
from fastapi.testclient import TestClient
from service.main import app

client = TestClient(app)

class TestUserAPI(TestCase):
    def test_get_all_users(self):
        response = client.get("/api/v1/user/list")
        self.assertEqual(response.status_code, 200)
        # self.assertGreater(len(response.json()["users"]), 0)

    def test_get_filtered_users(self):
        response = client.get("/api/v1/user/list?firstName=John&lastName=Doe")
        self.assertEqual(response.status_code, 200)
        # self.assertGreater(len(response.json()["users"]), 0)
        # for user in response.json()["users"]:
        #     self.assertEqual(user["first_name"], "John")
        #     self.assertEqual(user["last_name"], "Doe")

    def test_invalid_created_days(self):
        response = client.get("/api/v1/user/list?created_days=abc")
        self.assertEqual(response.status_code, 422)
        # self.assertIn("Invalid value for 'created_days'", response.text)

    def test_invalid_updated_days(self):
        response = client.get("/api/v1/user/list?updated_days=xyz")
        self.assertEqual(response.status_code, 422)
        # self.assertIn("Invalid value for 'updated_days'", response.text)



# # -*- coding: utf-8 -*-
# import json
# from fastapi.testclient import TestClient
# from service.main import app
# import pytest
# client = TestClient(app)
# from service.database.db_session import AsyncDatabaseSession



# def test_get_all_users():
#     response = client.get("/api/v1/user/list")
#     assert response.status_code == 200
#     # assert len(response.json()["users"]) > 0

# def test_get_filtered_users():
#     response = client.get("/api/v1/user/list?firstName=John&lastName=Doe")
#     assert response.status_code == 200
#     # assert len(response.json()["users"]) > 0
#     # for user in response.json()["users"]:
#     #     assert user["first_name"] == "John"
#     #     assert user["last_name"] == "Doe"

# def test_invalid_created_days():
#     response = client.get("/api/v1/user/list?created_days=abc")
#     assert response.status_code == 422
#     # assert "Invalid value for 'created_days'" in response.text

# def test_invalid_updated_days():
#     response = client.get("/api/v1/user/list?updated_days=xyz")
#     assert response.status_code == 422
#     # assert "Invalid value for 'updated_days'" in response.text
