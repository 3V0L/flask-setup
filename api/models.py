from api import db

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    projects_owned = db.relationship('Projects', backref='users', lazy=True)
    bids_sent = db.relationship('Bids', backref='users', lazy=True)


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(256), unique=False, nullable=False)
    contract_value = db.Column(db.Numeric(precision=2), nullable=False)
    percentage_return = db.Column(db.Numeric(precision=2), nullable=False)
    start_date = db.Column(db.Date, unique=False, nullable=False)
    end_date = db.Column(db.Date, unique=False, nullable=False)
    active = db.Column(db.Boolean, default=True)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email'),
        nullable=False)
    bids_received = db.relationship('Bids', backref='projects', lazy=True)


class Bids(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email'),
        nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'),
        nullable=False)
