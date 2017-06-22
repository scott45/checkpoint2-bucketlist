# import unittest
#
# import json
#
# # from config file
# from api.__init__ import app, EnvironmentName, databases
#
#
# class BucketlistTestCases(unittest.TestCase):
#     # testing client using testing environment
#     def setUp(self):
#         self.app = app.test_client()
#         EnvironmentName('TestingEnvironment')
#         databases.create_all()
#
#         # instance of a user directed to register route
#         payload = json.dumps({'username': 'scott', 'password': 'bucketlist'})
#         self.app.post('/bucketlist/api/v1/auth/register', data=payload)
#         credentials = self.app.post('/bucketlist/api/v1/auth/login', data=payload)
#         json_repr = json.loads(credentials.data.decode('utf-8'))
#         self.token = json_repr['Token']
#
#         # creating a bucketlist for testing purpose
#         self.payloads = json.dumps({'name': '1 Corinthians 13:13, Faith Hope and Love.'})
#
#     def tearDown(self):
#         databases.session.remove()
#         databases.drop_all()
#
#     def test_create_new_bucketlist(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         self.assertTrue(response.status_code == 201)
#
#     def test_create_new_bucketlist_without_name(self):
#         payload = json.dumps({'name': ''})
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=payload,
#                                  headers={"Authorization": self.token})
#
#     def test_create_existing_bucketlist(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#
#     def test_get_bucketlist(self):
#         response = self.app.post('/bucketlist/api/v1/bucketlist',
#                                  data=self.payloads, headers={"Authorization": self.token})
#         response = self.app.get('/bucketlist/api/v1/bucketlist',
#                                 headers={"Authorization": self.token})
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_non_existence_bucketlist(self):
#         response = self.app.get('/bucketlist/api/v1/bucketlist',
#                                 headers={"Authorization": self.token})
#         self.assertTrue(response.status_code == 200)
#
#     def test_get_bucketlist_by_id(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         response = self.app.get('/bucketlist/api/v1/bucketlist/1',
#                                 headers={"Authorization": self.token})
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_bucketlist_by_invalid_id(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         response = self.app.get('/bucketlist/api/v1/bucketlist/7',
#                                 headers={"Authorization": self.token})
#         self.assertEqual(response.status_code, 404)
#
#     def test__update_bucketlist(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         payload = json.dumps({'name': 'Hymn, This is my Fathers world,'})
#         response = self.app.put('/bucketlist/api/v1/bucketlist/1',
#                                 data=payload, headers={"Authorization": self.token})
#         self.assertEqual(response.status_code, 201)
#
#     def test_update_non_existence_bucketlist(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         payload = json.dumps({'name': 'Hymn, This is my Fathers world,'})
#         response = self.app.put('/bucketlist/api/v1/bucketlist/3',
#                                 data=payload, headers={"Authorization": self.token})
#         self.assertTrue(response.status_code == 404)
#
#     def test_delete_bucketlist(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         response = self.app.delete('/bucketlist/api/v1/bucketlist/1',
#                                    data=self.payloads, headers={"Authorization": self.token})
#         self.assertTrue(response.status_code, 201)
#
#     def test_delete_non_existence_bucketlist(self):
#         response = self.app.post('bucketlist/api/v1/bucketlist', data=self.payloads,
#                                  headers={"Authorization": self.token})
#         response = self.app.delete('/bucketlist/api/v1/bucketlist/3',
#                                    data=self.payloads, headers={"Authorization": self.token})
#         self.assertTrue(response.status_code, 404)
