import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from api.utils import json_abort

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    projects_owned = db.relationship(
        'Projects', backref='users', passive_deletes=True, lazy=True)
    bids_sent = db.relationship(
        'Bids', backref='users', passive_deletes=True, lazy=True)

    def save(self):
        """Save user"""
        if Users.query.filter_by(email=self.email).first():
            json_abort({'msg': 'User exists.'}, 409)
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def get_user(email, password):
        """Retrieve a user if their credentials are correct"""
        user = Users.query.filter_by(email=email).first()
        if user is None or not check_password_hash(user.password, password):
            json_abort({'msg': 'Invalid Email/Password entered'}, 401)
        return user


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(256), unique=False, nullable=False)
    contract_value = db.Column(db.Float(
        precision=16, asdecimal=True, decimal_return_scale=2), nullable=False)
    percentage_return = db.Column(db.Float(
        precision=16, asdecimal=True, decimal_return_scale=2), nullable=False)
    start_date = db.Column(db.Date, unique=False, nullable=False)
    end_date = db.Column(db.Date, unique=False, nullable=False)
    active = db.Column(db.Boolean, default=True)
    user_email = db.Column(db.String(120), db.ForeignKey(
        'users.email', ondelete='CASCADE'), nullable=False)
    bids_received = db.relationship(
        'Bids', backref='projects', passive_deletes=True, lazy=True)

    def save(self):
        """Save Project"""
        self.percentage_return = float(self.percentage_return)
        self.contract_value = float(self.contract_value)
        if self.contract_value < 1 or self.percentage_return < 1:
            json_abort(
                "Contract value and percentage return must"
                "be positive numbers", 400)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete Project"""
        db.session.delete(self)
        db.session.commit()

    def get_project(project_id, bid_amount):
        """Retrieve a project if it is valid"""
        project = Projects.query.filter_by(id=project_id).first()
        if project is None:
            json_abort(
                {'msg': 'This project is not available'}, 404)
        if project.end_date < datetime.date.today():
            project.active = False
            project.save()
            json_abort(
                {'msg': 'The end date for this project has passed.'
                        ' You can no longer bid on it.'}, 403)
        total_bids = 0
        for item in project.bids_received:
            total_bids = total_bids + float(item.amount)

        if float(project.contract_value) - total_bids < 1 or \
                project.end_date < datetime.date.today():
            project.active = False
            project.save()
            msg = {'msg': 'This project has been closed. No more'
                   ' investments are allowed'}
            json_abort(msg, 400)

        if (total_bids + bid_amount) > project.contract_value:
            msg = {'msg': f'The amount you want to invest is too much.'
                   ' You can only invest {}'.format(
                        (float(project.contract_value) - total_bids))}
            json_abort(msg, 400)

        return project

    def serialize(self):
        """Format data into JSON acceptable structure"""
        data = {
            "project_id": self.id,
            "description": self.description,
            "value": float(self.contract_value),
            "percentage_return": float(self.percentage_return),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "owner": Users.query.filter_by(
                email=self.user_email).first().username,
        }

        bids = []
        for item in self.bids_received:
            res = Bids.serialize(item)
            bids.append(res)
        data['bids'] = bids

        return data


class Bids(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(
        precision=16, asdecimal=True, decimal_return_scale=2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_email = db.Column(db.String(120), db.ForeignKey(
        'users.email', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id', ondelete='CASCADE'), nullable=False)

    def save(self):
        """Save bid"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete bid"""
        db.session.delete(self)
        db.session.commit()

    def get_bid(email, id):
        """Retrieve bid if valid"""
        bid = Bids.query.filter_by(
            user_email=email, id=id).first()
        if not bid:
            json_abort({'msg': 'You dont have access to this bid.'}, 401)
        return bid

    def serialize(self):
        """Format bid data for JSON"""
        return {
            "bid_id": self.id,
            "bidder_name": Users.query.filter_by(
                email=self.user_email).first().username,
            "amount": float(self.amount),
            "date": self.date,
            "project": self.project_id,
        }
