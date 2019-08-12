import datetime

from flask import json

from tests.base import BaseTestCase


class TestUser(BaseTestCase):
    
    def test_create_project(self):
        res = self.client.post('/project/create', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "name": "Project 123",
            "description": "This is a description",
            "value": 50000,
            "return": "34.677097",
            "end_date": datetime.date.today()+datetime.timedelta(days=10),
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn("Project Created Successfully." , str(res.data))
    
    def test_create_project_invalid_details(self):
        res = self.client.post('/project/create', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "name": "Pr",
            "description": "Th",
            "value": "string",
            "return": "string",
            "end_date": "not a date"
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn("Not a valid number." , str(res.data))
        self.assertIn("Length must be between" , str(res.data))
        self.assertIn("Not a valid date." , str(res.data))

    def test_create_project_invalid_user(self):
        res = self.client.post('/project/create', data=json.dumps({
            "email": "fake@mail.com",
            "password": "Password123",
            "name": "Project",
            "description": "Description of Project",
            "value": "4000",
            "return": "22",
            "end_date": datetime.date.today()+datetime.timedelta(days=10)
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn("Invalid Email/Password entered" , str(res.data))

    def test_edit_project(self):
        res = self.client.patch('/project/update', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "name": "Project",
            "description": "NEW Description",
            "project_id": self.project1.id,
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn("NEW Description" , str(res.data))
        self.assertIn("user1" , str(res.data))

    def test_edit_project_past_end_date(self):
        res = self.client.patch('/project/update', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "end_date": "2000/01/01",
            "project_id": self.project1.id,
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn(
            "The end date must be in the future." , str(res.data))

    def test_edit_project_amount_less_than_bids(self):
        res = self.client.patch('/project/update', data=json.dumps({
            "email": self.user2.email,
            "password": "Password2",
            "value": "1",
            "project_id": self.project2.id,
        }),
        content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertIn(
            "Cannot reduce amount below total bids" , str(res.data))

    def test_edit_project_invalid_details(self):
        res = self.client.patch('/project/update', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "name": "Pr",
            "value": 0,
            "project_id": self.project1.id,
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn("Length must be between" , str(res.data))
        self.assertIn("Must be between 1 and 1000000." , str(res.data))
    
    def test_update_someone_elses_project(self):
        res = self.client.patch('/project/update', data=json.dumps({
            "email": self.user2.email,
            "password": "Password2",
            "project_id": self.project1.id,
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn("Access Denied" , str(res.data))
    
    def test_delete_a_project(self):
        res = self.client.delete('/project/delete', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "project_id": self.project1.id,
        }),
        content_type='application/json')
        print(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Deleted" , str(res.data))

    def test_delete_a_project_non_existent(self):
        res = self.client.delete('/project/delete', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
            "project_id": 9999,
        }),
        content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn("Access Denied" , str(res.data))

    def test_get_all_projects(self):
        res = self.client.get(
            '/project/get-project', content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        assert len(data['data']) > 1

    def test_get_project_by_id(self):
        res = self.client.get(
            '/project/get-project?id={}'.format(self.project1.id),
            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data['data'][0]['value'], self.project1.contract_value)
    
    def test_get_project_nonexistent(self):
        res = self.client.get(
            '/project/get-project?id=99999',
            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['data']), 0)

    def test_get_my_projects(self):
        res = self.client.get('/project/my-projects', data=json.dumps({
            "email": self.user1.email,
            "password": "Password1",
        }),
        content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['data'][0]['project_id'], self.project1.id)


    
        
    