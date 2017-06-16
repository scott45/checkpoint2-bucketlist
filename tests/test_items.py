import unittest

# from config file
from api import app, EnvironmentName, databases

import json


class BucketlistItemsTestCases(unittest.TestCase):
    def setUp(self):
        # testing client using testing environment

        self.app = app.test_client()
        EnvironmentName('TestingEnvironment')
        databases.create_all()

        # instance of a user directed to register route
        payload = json.dumps({'username': 'scott', 'password': 'bucketlist'})
        self.app.post('/bucketlist/api/v1/auth/register', data=payload)
        credentials = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
        json_rep = json.loads(credentials.data)
        self.token = json_rep['Token']

        # creating a bucketlist for testing purpose
        self.payloads = json.dumps({'name': '1 Corinthians 13:13, Faith Hope and Love.'})
        self.itempayloads = json.dumps({'name': 'Romans 8:38, Nothing can separate us from the love of God.'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_create_new_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bucketlistitem successfully created", response.data.decode('utf-8'))

    def test_create_new_bucketlist_without_name(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        self.one = json.dumps({'name': ''})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.one, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bucketlistitem successfully created", response.data.decode('utf-8'))

    def test_create_existing_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertIn("Bucketlistitem has no name", response.data.decode('utf-8'))

    def test_create_items_for_non_existent_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/7/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)

    def test_edit_existing_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.itempayloads = json.dumps({'name': '1 john 4:8, God is Love.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bucketlistitem successfully edited", response.data.decode('utf-8'))

    def test_edit_non_existent_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.itempayloads = json.dumps({'name': '1 john 4:8, God is Love.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/4/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Bucketlistitem doesn't exist", response.data.decode('utf-8'))

    def test_delete_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.delete('bucketlist/api/v1/bucketlist/1/items',
                                   data=self.itempayloads, headers={"Authorization": self.token})
        self.assertIn("Bucketlistitem successfully deleted", response.data.decode('utf-8'))

    def test_delete_non_existent_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.delete('bucketlist/api/v1/bucketlist/3/items',
                                   data=self.itempayloads, headers={"Authorization": self.token})
        self.assertIn("Bucketlistitem doesn't exist", response.data.decode('utf-8'))

    def test_get_one_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.get('bucketlist/api/v1/bucketlist/1/items',
                                data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.get('bucketlist/api/v1/bucketlist/87/items',
                                data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)

    def test_get_bucketlist_by_invalid_token(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.get('bucketlist/api/v1/bucketlist/1/items',
                                data=self.itempayloads, headers={"Authorization": 'bad_token_here'})
        self.assertEqual(response.status_code, 401)
