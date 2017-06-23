import unittest
from api.__init__ import app, EnvironmentName, databases

import json


# tests all functionality of bucket items and there defined methods
class AuthenticationTestCases(unittest.TestCase):
    def setUp(self):

        # testing client using testing environment
        self.app = app.test_client()
        EnvironmentName('TestingEnvironment')
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests successful register
    def test_register_successfully(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 201)

    # tests register without password
    def test_register_without_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 401)

    # tests register with special characters
    def test_register_with_special_characters(self):
        payload = json.dumps({'username': '33s>^6?cot@@t', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 401)

    # tests register without username
    def register_without_username(self):
        payload = json.dumps({'username': '', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 400)

    # tests register with existing username
    def test_register_with_existing_username(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertIn('The Username already taken, register another name', response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)

    # tests register with short password
    def test_register_with_short_password(self):
        payload = json.dumps({'username': '', 'password': 'me'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 401)

    # tests registration route
    def test_registration_route(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        self.assertEqual(response.status_code, 201)

    # tests successful login
    def test_login_successful(self):
        payload = json.dumps({'username': 'scott', 'password': 'scott'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertIn('Successfully Logged in', response.data.decode('utf-8'))

    # tests register with invalid username
    def test_login__with_invalid_username(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'sctt', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    # tests register with wrong password
    def test_login_with_wrong_password(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'scott', 'password': 'somethings'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    # tests register with blank password
    def test_login_blank_password(self):
        payload = json.dumps({'username': 'scott', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    # tests register with blank username
    def test_login_blank_username(self):
        payload = json.dumps({'username': '', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    # tests register with invalid details
    def test_login_with_invalid_details(self):
        payload = json.dumps({'username': 'scott', 'password': 'something'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        payload = json.dumps({'username': 'scot', 'password': 'somethings'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 401)

    # tests login with special characters
    def test_login_with_special_characters_username(self):
        payload = json.dumps({'username': '#$^57dvcg', 'password': 'something'})
        response = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        self.assertAlmostEqual(response.status_code, 400)
