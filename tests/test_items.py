import unittest

# from config file
from api.__init__ import app, EnvironmentName, databases

import json


# tests all functionality of bucket items and there defined methods
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
        json_repr = json.loads(credentials.data.decode('utf-8'))
        self.token = json_repr['Token']

        # creating a bucketlist for testing purpose
        self.payloads = json.dumps({'name': '1 Corinthians 13:13, Faith Hope and Love.'})
        self.itempayloads = json.dumps({'name': 'Romans 8:38, Nothing can separate us from the love of God.'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a bucketlist item is successfully created
    def test_create_new_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)

    # tests that a bucketlist creation is not successful without name
    def test_create_new_bucketlist_without_name(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        self.one = json.dumps({'name': ''})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.one, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)

    # tests that a bucketlist creation is not successful with existing name
    def test_create_existing_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})

    # tests that a bucketlist creation is not successful without existing bucket
    def test_create_items_for_non_existent_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/7/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)

    # tests editing of an existing item
    def test_edit_existing_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.itempayloads = json.dumps({'name': '1 john 4:8, God is Love.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)

    # tests editing of a non existing item
    def test_edit_non_existent_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.itempayloads = json.dumps({'name': '1 john 4:8, God is Love.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/4/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)

    # tests deletion of an existing item
    def test_delete_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.delete('bucketlist/api/v1/bucketlist/1/items',
                                   data=self.itempayloads, headers={"Authorization": self.token})

    # tests deletion of a non existing item
    def test_delete_non_existent_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.delete('bucketlist/api/v1/bucketlist/3/items',
                                   data=self.itempayloads, headers={"Authorization": self.token})

    # tests retrieving of an existent item
    def test_get_one_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.get('bucketlist/api/v1/bucketlist/1/items',
                                data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 405)

    # tests retrieving of a non existent item
    def test_get_non_existent_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.get('bucketlist/api/v1/bucketlist/87/items',
                                data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 405)

    # tests retrieving of an item under an invalid token
    def test_get_bucketlist_by_invalid_token(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        response = self.app.get('bucketlist/api/v1/bucketlist/1/items',
                                data=self.itempayloads, headers={"Authorization": 'bad_token_here'})
        self.assertEqual(response.status_code, 405)
