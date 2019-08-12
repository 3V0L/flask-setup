import datetime
from flask import Blueprint, jsonify, request

from api.models import Users, Projects, Bids
from api.utils import RegisterUserSchema, CreateProjectSchema,\
    EmailPasswordSchema, UpdateProjectSchema, DeleteProjectSchema, \
    DeleteBidSchema, check_valid, BidSchema, UpdateBidSchema
    

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def home():
    """Returns home page for API"""
    return jsonify({'msg': 'Welcome to the API!'}), 200


@api.route('/register', methods=['POST'])
def register():
    """Register a user"""
    data = {
        'username': request.json.get('username'),
        'email': request.json.get('email'),
        'password': request.json.get('password'),
    }
    check_valid(RegisterUserSchema().validate(data))

    user = Users(
        username=data['username'], email=data['email'],
        password=data['password'])
    user.save()
    return jsonify({'message': 'Registered Successfully.'}), 201


@api.route('/project/create', methods=['POST'])
def create_project():
    """Register a user"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
        'name': request.json.get('name'),
        'description': request.json.get('description'),
        'contract_value': request.json.get('value'),
        'percentage_return': request.json.get('return'),
        'end_date': request.json.get('end_date'),
    }
    check_valid(CreateProjectSchema().validate(data))

    user = Users.get_user(data['email'], data['password'])
    project = Projects(
        name=data['name'], description=data['description'],
        contract_value=data['contract_value'],
        percentage_return=data['percentage_return'],
        start_date=datetime.date.today(), end_date=data['end_date'],
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
        projects = Projects.query.filter_by(
            id=id, active=True).all()
    else:
        projects = Projects.query.filter_by(active=True).all()
    res = list()
    for item in projects:
        if item.active == False:
            continue
        res.append(Projects.serialize(item))

    return jsonify({'data': res}), 200

@api.route('/project/my-projects', methods=['GET'])
def my_projects():
    """Get all projects"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
    }
    check_valid(EmailPasswordSchema().validate(data))

    user = Users.get_user(data['email'], data['password'])
    projects = Projects.query.filter_by(user_email=user.email)
    res = list()
    for item in projects:
        if item.active == False:
            continue
        res.append(Projects.serialize(item))

    return jsonify({'data': res}), 200

@api.route('/project/update', methods=['PATCH'])
def update_projects():
    """Get all projects"""
    changes = {
        "name": request.json.get('name'),
        "description": request.json.get('description'),
        "contract_value": request.json.get('value'),
        "percentage_return": request.json.get('percentage_return'),
        "end_date": request.json.get('end_date'),
    }
    data = changes.copy()
    data.update({
        'email': request.json.get('email'),
        'password': request.json.get('password'),
        'project_id': request.json.get('project_id'),
    })
    check_valid(UpdateProjectSchema().validate(data))
   
    user = Users.get_user(data['email'], data['password'])
    projects = Projects.query.filter_by(
        user_email=user.email, id=data['project_id']).first()

   
    total_bids = 0
    if projects:
        for item in projects.bids_received:
            total_bids = total_bids + float(item.amount)

        if changes['contract_value'] != None and \
                float(changes['contract_value']) < total_bids:
            return jsonify({
                "msg": "Cannot reduce amount below total bids ({})".format(
                    total_bids)}), 400

        for key in changes:
            if changes[key] is None:
                continue
            setattr(projects, key, changes[key])
        projects.save()

        return jsonify({
            'msg': "Success",
            'data': projects.serialize()
            }), 200
    return jsonify({'msg': "Access Denied."}), 401


@api.route('/project/delete', methods=['DELETE'])
def delete_projects():
    """Get all projects"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
        'project_id': request.json.get('project_id'),
    }
    check_valid(DeleteProjectSchema().validate(data))

    user = Users.get_user(data['email'], data['password'])
    project = Projects.query.filter_by(
        user_email=user.email, id=data['project_id']).first()
    if project is None:
        return jsonify({'msg': "Access Denied"}), 401
    project.delete()

    return jsonify({'msg': "Deleted"}), 200


@api.route('/bid/create', methods=['POST'])
def bid_to_project():
    """Bid to fund a project"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
        'amount': request.json.get('amount'),
        'project_id': request.json.get('project_id'),
    }
    check_valid(BidSchema().validate(data))

    data['amount'] = float(data['amount'])
    user = Users.get_user(data['email'], data['password'])
    project = Projects.get_project(
        request.json['project_id'], data['amount'])

    bid = Bids(
        amount=data['amount'], date=datetime.date.today(),
        user_email=user.email, project_id=project.id,)
    bid.save()

    data['user_email'] = user.email
    data['project_id'] = project.id
    data['bid_id'] = bid.id
    data['potential_profit_margin'] = "{0:.2f}".format(
        float(project.percentage_return) / 100 * data['amount'])

    return jsonify({
        'message': 'Bid Created Successfully.',
        'data': data,
        }), 201


@api.route('/bid/update', methods=['PATCH'])
def update_bid():
    """Get all projects"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
        'amount': request.json.get('amount'),
        'bid_id': request.json.get('bid_id'),
    }
    check_valid(UpdateBidSchema().validate(data))

    user = Users.get_user(data['email'], data['password'])
    bid = Bids.get_bid(data['email'], data['bid_id'])
    project = Projects.get_project(bid.project_id, 0)
    
    total_bids = 0
    current_amnt = float(bid.amount)
    new_amnt = float(request.json['amount'])

    for item in project.bids_received:
        total_bids = total_bids + float(item.amount)

    total_bids = total_bids - current_amnt + new_amnt
    if float(project.contract_value) < total_bids:
        return jsonify({
            "msg": "The amount added is too much. Reduce it by {}".format(
                (total_bids - float(project.contract_value)))}), 400

    bid.amount = new_amnt
    bid.date = datetime.date.today()
    bid.save()

    return jsonify({
        'message': 'Updated Bid.',
        'data': bid.serialize(),
        }), 200


@api.route('/bid/delete', methods=['DELETE'])
def delete_bid():
    """Get all projects"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
        'bid_id': request.json.get('bid_id'),
    }
    err = DeleteBidSchema().validate(data)
    if err:
        return jsonify(err), 400
    user = Users.get_user(data['email'], data['password'])

    bid = Bids.query.filter_by(
        user_email=user.email, id=data['bid_id']).first()
    if not bid:
        return jsonify({'msg': "This bid was not found"}), 404

    # Retrieve project to check whether project still active
    project = Projects.get_project(bid.project_id, 0)
    
    bid.delete()

    return jsonify({'msg': "Bid Deleted"}), 200

@api.route('/bid/my-bids', methods=['GET'])
def my_bids():
    """Get all projects"""
    data = {
        'email': request.json.get('email'),
        'password': request.json.get('password'),
    }
    err = EmailPasswordSchema().validate(data)
    if err:
        return jsonify(err), 400
    user = Users.get_user(request.json['email'], request.json['password'])
    bid = Bids.query.filter_by(user_email=user.email).all()

    res = []
    for item in bid:
        item = item.serialize()
        project = Projects.query.filter_by(id=item['project']).first()
        project = project.serialize()
        project.pop('bids')
        item['project'] = project
        res.append(item)

    return jsonify({'data': res }), 200
