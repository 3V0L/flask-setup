import datetime

from flask import json

from tests.base import BaseTestCase


class TestUser(BaseTestCase):

    def test_bid_to_project(self):
        res = self.client.post(
            '/bid/create',
            data=json.dumps({
                "email": self.user2.email,
                "password": "Password2",
                "amount": "100",
                "project_id": self.project1.id
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn("Bid Created Successfully.", str(res.data))

    def test_bid_to_project_invalid_amount(self):
        res = self.client.post(
            '/bid/create',
            data=json.dumps({
                "email": self.user2.email,
                "password": "Password2",
                "amount": "10000000",
                "project_id": self.project1.id
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn(
            "Must be between 1 and 1000000.", str(res.data))

    def test_bid_to_nonexistent_project(self):
        res = self.client.post(
            '/bid/create',
            data=json.dumps({
                "email": self.user2.email,
                "password": "Password2",
                "amount": "10000000",
                "project_id": self.project1.id
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn(
            "Must be between 1 and 1000000.", str(res.data))

    def test_bid_to_project_excess_amount(self):
        res = self.client.post(
            '/bid/create',
            data=json.dumps({
                "email": self.user2.email,
                "password": "Password2",
                "amount": "100000",
                "project_id": self.project1.id
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn(
            "The amount you want to invest is too much.", str(res.data))

    def test_bid_to_project_nonexistent(self):
        res = self.client.post(
            '/bid/create',
            data=json.dumps({
                "email": self.user2.email,
                "password": "Password2",
                "amount": "100000",
                "project_id": 99
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 404)
        self.assertIn("This project is not available", str(res.data))

    def test_get_my_bids(self):
        res = self.client.get(
            '/bid/my-bids',
            data=json.dumps({
                "email": self.user1.email,
                "password": "Password1",
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.user1.username, str(res.data))

    def test_update_bids(self):
        res = self.client.patch(
            '/bid/update',
            data=json.dumps({
                "email": self.user1.email,
                "password": "Password1",
                "bid_id": self.bid.id,
                "amount": 300
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.user1.username, str(res.data))

    def test_update_bid_amount_too_high(self):
        res = self.client.patch(
            '/bid/update',
            data=json.dumps({
                "email": self.user1.email,
                "password": "Password1",
                "bid_id": self.bid.id,
                "amount": 30000
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn("The amount added is too much", str(res.data))

    def test_update_bid_nonexistent(self):
        res = self.client.patch(
            '/bid/update',
            data=json.dumps({
                "email": self.user1.email,
                "password": "Password1",
                "bid_id": 9999,
                "amount": 30000
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn(
            "You dont have access to this bid.", str(res.data))

    def test_delete_bid(self):
        res = self.client.delete(
            '/bid/delete',
            data=json.dumps({
                "email": self.user1.email,
                "password": "Password1",
                "bid_id": self.bid.id,
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Bid Deleted", str(res.data))

    def test_delete_bid_nonexistent(self):
        res = self.client.delete(
            '/bid/delete',
            data=json.dumps({
                "email": self.user1.email,
                "password": "Password1",
                "bid_id": 999,
            }),
            content_type='application/json')
        self.assertEqual(res.status_code, 404)
        self.assertIn("This bid was not found", str(res.data))
