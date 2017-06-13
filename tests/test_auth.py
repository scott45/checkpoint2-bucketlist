import unittest
from application import app, EnvironmentName

import json


class AuthenticationTestCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_register_successfully(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.application.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Registration successful', response.data.decode('utf-8'))

    def test_register_without_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.application.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn("Password field is blank", response.data.decode('utf-8'))

    def test_register_with_special_characters(self):
        pass

    def register_without_username(self):
        pass

    def test_register_with_existing_username(self):
        pass

    def test_register_with_short_password(self):
        pass

    def test_registration_route(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.application.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_wrong_registration_route(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.application.post('/bucketlist/api/v1/auth/regstr', data=payload)
        self.assertAlmostEqual(response.status_code, 404)

    def test_login__with_invalid_username(self):
        payload = json.dumps({'username': 'sctt', 'password': 'something'})
        response = self.applications.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertAlmostEqual(response.status_code, 404)
        self.assertIn("Unknown username, please enter a valid username", response.data.decode('utf-8'))

    def test_login_with_wrong_password(self):
        pass

    def test_login_successful(self):
        pass

    def test_login_blank_password(self):
        pass

    def test_login_blank_username(self):
        pass

    def test_login_with_invalid_details(self):
        pass

    def test_login_with_special_characters_username(self):
        pass
