import datetime
from flask import Blueprint, jsonify, request

from api.models import Users, Projects, Bids

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def home():
    """Returns home page for API"""
    return jsonify({'msg': 'Welcome to the API!'}), 200


@api.route('/register', methods=['POST'])
def register():
    """Register a user"""
    data = {
        'username': request.json['username'],
        'email': request.json['email'],
        'password': request.json['password'],
    }
    # Validate here
    user = Users(
        username=data['username'], email=data['email'],
        password=data['password'])
    user.save()
    return jsonify({'message': 'Registered Successfully.'}), 201


@api.route('/project/create', methods=['POST'])
def create_project():
    """Register a user"""
    user = Users.get_user(request.json['email'], request.json['password'])

    data = {
        'name': request.json['name'],
        'description': request.json['description'],
        'contract_value': float(request.json['value']),
        'percentage_return': float(request.json['return']),
        'start_date': request.json['start_date'],
        'end_date': request.json['end_date'],
    }
   
    project = Projects(
        name=data['name'], description=data['description'],
        contract_value=data['contract_value'],
        percentage_return=data['percentage_return'],
        start_date=data['start_date'], end_date=data['end_date'],
        user_email=user.email)
    project.save()

    data['project_id'] = project.id

    return jsonify({
        'message': 'Project Created Successfully.',
        'data': data,
        }), 201

@api.route('/project/get-project', methods=['GET'])
def get_projects():
    """Get all projects"""
    id = request.args.get('id')
    if id:
        projects = Projects.query.filter_by(id=id)
    else:
        projects = Projects.query.all()
    res = list()
    for item in projects:
        if item.active == False:
            continue
        res.append(Projects.serialize(item))

    return jsonify({'data': res}), 200

@api.route('/project/my-projects', methods=['GET'])
def my_projects():
    """Get all projects"""
    user = Users.get_user(request.json['email'], request.json['password'])
    projects = Projects.query.all()
    res = list()
    for item in projects:
        if item.active == False:
            continue
        data = {
            "project_id": item.id,
            "description": item.description,
            "value": float(item.contract_value),
            "percentage_return": float(item.percentage_return),
            "start_date": item.start_date,
            "end_date": item.end_date,
            "owner": Users.query.filter_by(
                email=item.user_email).first().username,
            "bids": item.bids_received,
        }
        res.append(data)

    return jsonify({'data': res}), 200


@api.route('/bid/create', methods=['POST'])
def bid_to_project():
    """Bid to fund a project"""
    data = {
        'amount': decimal(request.json['amount']),
        'date': str(datetime.date.today()),
    }

    user = Users.get_user(request.json['email'], request.json['password'])
    project = Projects.get_project(
        request.json['project_id'], data['amount'])

    bid = Bids(
        amount=data['amount'], date=data['date'],
        user_email=user.email, project_id=project.id,)
    bid.save()

    data['user_email'] = user.email
    data['project_id'] = project.id
    data['bid_id'] = bid.id
    data['potential_profit_margin'] = "{0:.2f}".format(
        float(project.percentage_return) / 100 * data['amount'])

    return jsonify({
        'message': 'Project Created Successfully.',
        'data': data,
        }), 201