import unittest

# parses json to string or files (or python dict and []
import json

# from config file
from api.__init__ import app, EnvironmentName, databases

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''


# tests all functionality of bucketlist.py and there defined methods
class BucketlistTestCases(unittest.TestCase):
    # testing client using testing environment
    def setUp(self):
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

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a bucketlist is successfully created
    def test_create_new_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        self.assertTrue(response.status_code == 201)

    # tests creation of bucket fails without name
    def test_create_new_bucketlist_without_name(self):
        payload = json.dumps({'name': ''})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload,
                                 headers={"Authorization": self.token})  #
        self.assertEqual(response.status_code, 400)

    # tests creation of bucket fails with existing name
    def test_create_existing_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})  #
        self.assertEqual(response.status_code, 409)

    # tests that a bucket successfully created is retrieved
    def test_get_bucketlist(self):
        response = self.app.post('/bucketlist/api/v1/bucketlist',
                                 data=self.payloads, headers={"Authorization": self.token})
        response = self.app.get('/bucketlist/api/v1/bucketlist',
                                headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)

    # tests that a bucket not successfully created is not found
    def test_get_bucketlist_while_database_empty(self):
        response = self.app.get('/bucketlist/api/v1/bucketlist',
                                headers={"Authorization": self.token})
        self.assertTrue(response.status_code == 200)
        self.assertIn('No bucketlist has been created', response.data.decode('utf-8'))  #

    # tests getting a bucket by id
    def test_get_bucketlist_by_id(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.get('/bucketlist/api/v1/bucketlist/1',
                                headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)

    # tests getting a bucket by invalid id fails
    def test_get_bucketlist_by_invalid_id(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.get('/bucketlist/api/v1/bucketlist/7',
                                headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 404)

    # tests updating a bucket
    def test__update_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        payload = json.dumps({'name': 'Hymn, This is my Fathers world,'})
        response = self.app.put('/bucketlist/api/v1/bucketlist/1',
                                data=payload, headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)

    # tests updating a non existent bucket fails
    def test_update_non_existence_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        payload = json.dumps({'name': 'Hymn, This is my Fathers world,'})
        response = self.app.put('/bucketlist/api/v1/bucketlist/3',
                                data=payload, headers={"Authorization": self.token})
        self.assertTrue(response.status_code == 404)

    # tests deleting a bucket
    def test_delete_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.delete('/bucketlist/api/v1/bucketlist/1',
                                   data=self.payloads, headers={"Authorization": self.token})
        self.assertTrue(response.status_code, 200)  #

    # tests deleting a non existent bucket fails
    def test_delete_non_existence_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.delete('/bucketlist/api/v1/bucketlist/3',
                                   data=self.payloads, headers={"Authorization": self.token})
        self.assertTrue(response.status_code, 404)

    # tests that a pagination default is 20
    def test_get_pagination_default(self):
        response = self.app.get('/bucketlist/api/v1/bucketlist?limit=20',
                                headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)  #

    # tests search bucket by name
    def test_search_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.get('/bucketlist/api/v1/bucketlist?q=Faith',
                                headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)  #

    # tests search bucket by name
    def test_search_non_existent_bucketlist(self):
        response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
                                 headers={"Authorization": self.token})
        response = self.app.get('/bucketlist/api/v1/bucketlist?q=Wikedzi&limit=100',
                                headers={"Authorization": self.token})
        self.assertIn('The bucketlist you searched does not exist',
                      response.data.decode('utf-8'))  #
