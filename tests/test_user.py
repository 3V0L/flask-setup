from flask import json

from tests.base import BaseTestCase


class TestUser(BaseTestCase):
    
    def test_user_registration(self):
        register = self.client.post('/register', data=json.dumps({
            "username": "Testing",
            "email": "sample123@mail.com",
            "password": "Sample123"
        }),
        content_type='application/json')
        self.assertEqual(register.status_code, 201)
        self.assertIn("Registered Successfully" , str(register.data))
    
    def test_duplicate_user_registration(self):
        register = self.client.post('/register', data=json.dumps({
            "username": "Duplicate",
            "email": self.user1.email,
            "password": "Sample123"
        }),
        content_type='application/json')
        self.assertEqual(register.status_code, 409)
        self.assertIn("User exists" , str(register.data))

    def test_user_registration_invalid_data(self):
        register = self.client.post('/register', data=json.dumps({
            "username": "No",
            "email": "mail",
            "password": "pass"
        }),
        content_type='application/json')
        print(register.data)
        self.assertEqual(register.status_code, 400)
        self.assertIn("Not a valid email address" , str(register.data))
