import json

from flask import request
from flask_restplus import Resource

from app.initializations import *
from model import model

db.create_all()


@name_space.route("/v1/user/<string:id>")
class User(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the person'})
    def get(self, id):
        headers = request.headers.get('Authorization')
        print('headers: ', headers)
        usr = model.User.get_by_id(id)
        if usr is None:
            return name_space.abort(400, status="user not found", statusCode="400")

        return usr.to_json()

    @app.expect(Person)
    def post(self, id):
        body = request.data
        kwargs = json.loads(body)
        kwargs['user_id'] = id
        usr = model.User(**kwargs)
        usr.persist()
        return usr.to_json()


@name_space.route("/v1/auth")
class Auth(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(Auth)
    def post(self):
        body = request.data
        kwargs = json.loads(body)
        kwargs['registration_key'] = ''
        auth = model.Authorization(**kwargs)
        return auth.validate()


@name_space.route("/v1/dashboard/<string:role>")
class Dashboard(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def get(self, role):
        print("Role: ", role)
        d = model.Dashboard(role)
        return d.fetch()


@name_space.route("/v1/register/<string:registration_key>")
class Register(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(Registration)
    def post(self, registration_key):
        body = request.data
        kwargs = json.loads(body)
        kwargs['registration_key'] = registration_key
        model.User.register(**kwargs)
        return {"message": "success"}


@name_space.route("/v1/help/<string:id>")
class Help(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(Help)
    def post(self, id):
        print("id:", id)
        body = request.data
        kwargs = json.loads(body)
        print(kwargs)
        is_closed = kwargs['closed']

        if kwargs['description'] is None and kwargs['note'] is None:
            return name_space.abort(400, status="bad input: Description and Notes both cannot be empty",
                                    statusCode="400")

        if kwargs['location'] is None and kwargs['address'] is None:
            return name_space.abort(400, status="bad input: Lat_Long and Address both cannot be empty",
                                    statusCode="400")

        auth_data = model.Authorization.verify_signature(kwargs['token'])
        user = auth_data['user']
        print('user: ', user)
        if id is None or str(id).isspace():
            #     Create new one
            if user is None:
                return name_space.abort(400, status="Failed to authenticate", statusCode="400")

            kwargs['requestor_id'] = user
            del kwargs['token']
            del kwargs['closed']
            h = model.Help(**kwargs)
            h.persist()
            return h.to_json()

        h = model.Help.get_by_id(id)
        if h is None:
            return name_space.abort(400, status="Unable to fetch the given help id", statusCode="400")

        h.respond(kwargs['note'], user)
        h.persist()

        return h.to_json()
