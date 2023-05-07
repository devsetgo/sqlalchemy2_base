# -*- coding: utf-8 -*-
import json
from datetime import datetime
from unittest import TestCase
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from service.main import app

client = TestClient(app)


class TestUserAPI(TestCase):
    def test_get_all_users(self):
        response = client.get("/api/v1/user/list")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()

    def test_filter_by_first_name(self):
        response = client.get("/api/v1/user/list?first_name=John")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     assert user["first_name"] == "John"

    def test_filter_by_last_name(self):
        response = client.get("/api/v1/user/list?last_name=Doe")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     assert user["last_name"] == "Doe"

    def test_filter_by_email(self):
        response = client.get("/api/v1/user/list?email=john.doe@example.com")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     assert user["email"] == "john.doe@example.com"

    def test_filter_by_is_active(self):
        response = client.get("/api/v1/user/list?is_active=true")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     assert user["is_active"] == True

    def test_filter_by_is_approved(self):
        response = client.get("/api/v1/user/list?is_approved=true")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     assert user["is_approved"] == True

    def test_filter_by_created_days(self):
        response = client.get("/api/v1/user/list?created_days=7")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     created_date = datetime.strptime(user["date_created"], "%Y-%m-%dT%H:%M:%S.%fZ")
        #     assert (datetime.utcnow() - created_date).days <= 7

    def test_filter_by_updated_days(self):
        response = client.get("/api/v1/user/list?updated_days=7")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # for user in response.json()["users"]:
        #     updated_date = datetime.strptime(user["date_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
        #     assert (datetime.utcnow() - updated_date).days <= 7

    def test_limit_offset(self):
        response = client.get("/api/v1/user/list?limit=10&offset=20")
        self.assertEqual(response.status_code, 200)
        # assert "query_data" in response.json()
        # assert "users" in response.json()
        # assert len(response.json()["users"]) == 10
        # assert response.json()["query_data"]["offset"] == 20
        # assert response.json()["query_data"]["limit"] == 10


#########################################################################
# import json
# from unittest import TestCase
# import pytest
# from fastapi.testclient import TestClient

# from service.main import app
# from service.database import db_session

# client = TestClient(app)


# @pytest.mark.asyncio
# async def test_get_all_users():
#     response = client.get("/api/v1/user/list")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()


# @pytest.mark.asyncio
# async def test_filter_by_first_name():
#     response = client.get("/api/v1/user/list?first_name=John")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     assert user["first_name"] == "John"


# @pytest.mark.asyncio
# async def test_filter_by_last_name():
#     response = client.get("/api/v1/user/list?last_name=Doe")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     assert user["last_name"] == "Doe"


# @pytest.mark.asyncio
# async def test_filter_by_email():
#     response = client.get("/api/v1/user/list?email=john.doe@example.com")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     assert user["email"] == "john.doe@example.com"


# @pytest.mark.asyncio
# async def test_filter_by_is_active():
#     response = client.get("/api/v1/user/list?is_active=true")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     assert user["is_active"] == True


# @pytest.mark.asyncio
# async def test_filter_by_is_approved():
#     response = client.get("/api/v1/user/list?is_approved=true")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     assert user["is_approved"] == True


# @pytest.mark.asyncio
# async def test_filter_by_created_days():
#     response = client.get("/api/v1/user/list?created_days=7")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     created_date = datetime.strptime(user["date_created"], "%Y-%m-%dT%H:%M:%S.%fZ")
#     #     assert (datetime.utcnow() - created_date).days <= 7


# @pytest.mark.asyncio
# async def test_filter_by_updated_days():
#     response = client.get("/api/v1/user/list?updated_days=7")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # for user in response.json()["users"]:
#     #     updated_date = datetime.strptime(user["date_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
#     #     assert (datetime.utcnow() - updated_date).days <= 7


# @pytest.mark.asyncio
# async def test_limit_offset():
#     response = client.get("/api/v1/user/list?limit=10&offset=20")
#     assert response.status_code == 200
#     # assert "query_data" in response.json()
#     # assert "users" in response.json()
#     # assert len(response.json()["users"]) == 10
#     # assert response.json()["query_data"]["offset"] == 20
#     # assert response.json()["query_data"]["limit"] == 10
