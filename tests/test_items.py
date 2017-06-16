import unittest

# from config file
from app import app, EnvironmentName, databases

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

        # creating a bucketlist for testing purpose
        self.token = json_rep['Token']
        self.itempayloads = json.dumps({'name': 'Romans 8:38, Nothing can separate us from the love of God.'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_create_new_bucketlistitem(self):
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items',
                                 data=self.itempayloads, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bucketlistitem successfully created", response.data.decode('utf-8'))

    def test_create_existing_bucketlistitem(self):
        pass

    def test_create_items_for_unexisting_bucketlist(self):
        pass

    def test_update_existing_bucketlistitem(self):
        pass

    def test_update_unexisting_bucketlistitem(self):
        pass

    def test_delete_bucketlistitem(self):
        pass

    def test_delete_unexisting_bucketlistitem(self):
        pass

    def test_get_one_bucketlistitem(self):
        pass

    def test_get_unexisting_bucketlistitem(self):
        pass

    def test_get_bucketlist_by_id(self):
        pass

    def test_get_bucketlist_by_invalid_id(self):
        pass

    def test_create_new_bucketlist_without_title(self):
        pass
