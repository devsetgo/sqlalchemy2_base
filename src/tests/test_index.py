# -*- coding: utf-8 -*-
import unittest

from fastapi import status
from fastapi.testclient import TestClient

from service.main import app

client = TestClient(app)


class RootEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_redirect_response(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.headers["location"], "/docs")
