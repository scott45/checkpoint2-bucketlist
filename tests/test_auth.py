import unittest

# from config file
from api import app, EnvironmentName, databases

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
        self.assertIn('Registration successful', response.data.decode('utf-8'))

    def test_register_without_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn("Password field is blank, register with one", response.data.decode('utf-8'))

    def test_register_with_special_characters(self):
        payload = json.dumps({'username': '33s?cot@@t', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn("username cannot contain special characters", response.data.decode('utf-8'))

    def register_without_username(self):
        payload = json.dumps({'username': '', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn("username cannot be empty", response.data.decode('utf-8'))

    def test_register_with_existing_username(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn("Username has already been used, Use another", response.data.decode('utf-8'))

    def test_register_with_short_password(self):
        payload = json.dumps({'username': '', 'password': 'me'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn("Password is too short, use a longer one", response.data.decode('utf-8'))

    def test_registration_route(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_wrong_registration_route(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/regstr', data=payload)
        self.assertAlmostEqual(response.status_code, 404)

    def test_login_successful(self):
        payload = json.dumps({'username': 'scott', 'password': 'scott'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertIn("login successful", response.data.decode('utf-8'))

    def test_login__with_invalid_username(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'sctt', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)
        self.assertIn("Unknown username, please enter a valid username", response.data.decode('utf-8'))

    def test_login_with_wrong_password(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'scott', 'password': 'somethings'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)
        self.assertIn("Incorrect password, please enter a valid password", response.data.decode('utf-8'))

    def test_login_blank_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)
        self.assertIn("login unsuccessful, password field is empty", response.data.decode('utf-8'))

    def test_login_blank_username(self):
        payload = json.dumps({'username': '', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)
        self.assertIn("login unsuccessful, username field is empty", response.data.decode('utf-8'))

    def test_login_with_invalid_details(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'scot', 'password': 'somethings'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)
        self.assertIn("Incorrect login credentials, please enter a valid username and password",
                      response.data.decode('utf-8'))

    def test_login_with_special_characters_username(self):
        payload = json.dumps({'username': '#$^57dvcg', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)
        self.assertIn("login unsuccessful, username contains special characters", response.data.decode('utf-8'))
