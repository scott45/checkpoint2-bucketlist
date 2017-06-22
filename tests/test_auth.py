import unittest
from api.__init__ import app, EnvironmentName, databases

import json


class AuthenticationTestCases(unittest.TestCase):
    def setUp(self):

        # testing client using testing environment
        self.app = app.test_client()
        EnvironmentName('DevelopmentEnvironment')
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_register_successfully(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_register_without_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 401)

    def test_register_with_special_characters(self):
        payload = json.dumps({'username': '33s?cot@@t', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 401)

    def register_without_username(self):
        payload = json.dumps({'username': '', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 400)

    def test_register_with_existing_username(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn('The Username already taken, register another name', response.data.decode('utf-8'))

    def test_register_with_short_password(self):
        payload = json.dumps({'username': '', 'password': 'me'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 400)

    def test_registration_route(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_login_successful(self):
        payload = json.dumps({'username': 'scott', 'password': 'scott'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertIn('Successfully Logged in', response.data.decode('utf-8'))

    def test_login__with_invalid_username(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'sctt', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    def test_login_with_wrong_password(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'scott', 'password': 'somethings'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    def test_login_blank_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)

    def test_login_blank_username(self):
        payload = json.dumps({'username': '', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)

    def test_login_with_invalid_details(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'scot', 'password': 'somethings'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    def test_login_with_special_characters_username(self):
        payload = json.dumps({'username': '#$^57dvcg', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)
