import datetime
from unittest import TestCase

from api import create_app
from api.models import db, Users, Projects, Bids


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()
        with self.app.app_context():
            db.create_all()
        self.user1 = Users(
            username='user1', email='user1@mail.com',
            password='Password1')
        self.user1.save()
        self.user2 = Users(
            username='user2', email='user2@mail.com',
            password='Password2')
        self.user2.save()
        self.project1 = Projects(
            name="User1's Project", description='sample project',
            contract_value='5000',
            percentage_return='22',
            start_date=datetime.date.today(),
            end_date=datetime.date.today()+datetime.timedelta(days=10),
            user_email=self.user1.email)
        self.project1.save()
        self.project2 = Projects(
            name="User2's Project", description='sample project',
            contract_value='3000',
            percentage_return='10',
            start_date=datetime.date.today(),
            end_date=datetime.date.today()+datetime.timedelta(days=10),
            user_email=self.user2.email)
        self.project2.save()
        self.bid = Bids(
            amount='200', date=datetime.date.today(),
            user_email=self.user1.email, project_id=self.project2.id,)
        self.bid.save()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
