import enum
import uuid
from datetime import datetime, timedelta, timezone
from json import JSONEncoder

import jwt

from app.initializations import db
from model.email import send_email


class Roles(enum.Enum):
    Admin = 'Admin'
    Donor = 'Donor'
    Needy = 'Needy'


class HelpStatus(enum.Enum):
    Open = 'Open'
    Closed = 'Closed'
    Responded = 'Responded'


html_template = """
<p>Thank you!! for registering at helpyourneighbor.org</p>
<p>Please complete registration by clicking this link.</p>
<p><strong><a href="https://help_your_neighbor.org/registration/REGISTRATION_KEY">https://help_your_neighbor.org/registration/REGISTRATION_KEY</a>&nbsp;</strong></p>
"""


class Authorization(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    registration_key = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, registration_key):
        self.username = username
        self.password = password
        self.registration_key = registration_key

    def persist(self):
        db.session.add(self)
        db.session.commit()

    def validate(self):
        # TODO:  Read the database validate the hash. Send the ACCESS_TOKEN
        usr = self.query.filter_by(username=self.username).first()
        if usr is None:
            raise Exception('user not found: %s', self.username)

        if usr.password is None or usr.password != self.password:
            raise Exception('user_id or password is incorrect')

        message = {
            'iss': 'https://helpyourneighbor.com/',
            'sub': self.username,
            'reg': self.registration_key,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        }

        encoded_jwt = jwt.encode(message, self.get_secret(), algorithm=self.get_alogorithm())
        access_token = {
            "access_token": encoded_jwt.decode()
        }
        return access_token

    @classmethod
    def get_alogorithm(cls):
        return 'HS256'

    @classmethod
    def get_secret(cls):
        # with open('rsa_private_key.pem', 'rb') as fh:
        #     signing_key = jwk_from_pem(fh.read())
        signing_key = "a random, long, sequence of characters that only the server knows"
        return signing_key

    @classmethod
    def verify_signature(cls, token):
        return jwt.decode(token, cls.get_secret(), algorithms=[cls.get_alogorithm()])


class Dashboard:

    def __init__(self, role):
        self.role = role
        self.needy_count = 0
        self.donor_count = 0
        self.total_help_requests = 0
        self.total_help_responses = 0

    def fetch(self):
        self.needy_count = 100
        self.donor_count = 50
        self.total_help_requests = 10
        return


class Help(db.Model):
    uuid = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    created_time = db.Column(db.String(80))
    response_time = db.Column(db.String(80))
    requestor_id = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80))
    location = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80))
    response_notes = db.Column(db.String(8000))

    def __init__(self, description, requestor_id, address=None):
        self.uuid = uuid.uuid4()
        self.description = description
        self.created_time = str(datetime.now())
        self.requestor_id = requestor_id
        self.status = HelpStatus.Open
        self.response_notes = ''
        self.address = address

    def respond(self, note, donor):
        self.response_time = datetime.now()
        response = f'<note:{note},donor:{donor}>,'
        self.response_notes = self.response_notes + response
        self.status = HelpStatus.Responded
        self.persist()

    def close(self):
        self.status = "CLOSED"
        self.persist()

    def persist(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(self, id):
        help = self.query.filter_by(uuid=id).first()
        if help is None:
            raise Exception('Unable to get the help request')

        return help

    @classmethod
    def get_all(self):
        helps = self.query.all()
        if helps is None or len(helps) == 0:
            raise Exception('No records found')

        return helps


class User(db.Model, JSONEncoder):
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120))
    email = db.Column(db.String(80), unique=True, nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False)
    lat_long = db.Column(db.String(120))
    role = db.Column(db.String(80))
    user_id = db.Column(db.String(80), primary_key=True)
    registration_key = db.Column(db.String(80))

    def __init__(self, first_name, last_name, address, email, mobile, lat_long, user_id, role=Roles.Needy):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.mobile = mobile
        self.lat_long = lat_long
        self.role = role
        self.user_id = user_id

    def persist(self):
        self.registration_key = str(uuid.uuid4())
        html_message = html_template.replace('REGISTRATION_KEY', self.registration_key, -1)
        print(self)
        print('during registration html_message: ', html_message)
        send_email(self.email, subject='help your neighbor registration', html_content=html_message)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def register(self, username, password, registration_key):
        usr = self.query.filter_by(user_id=username).first()
        if password is None or registration_key is None:
            raise Exception('Password or Registration Key is empty')

        if registration_key != usr.registration_key:
            raise Exception('Registration Key did not match')

        auth = Authorization(username=username, password=password, registration_key=registration_key)
        auth.persist()

    @classmethod
    def get_by_id(cls, user_id):
        usr = cls.query.filter_by(user_id=user_id).first()
        if usr is None:
            print('unable to find user by id')
            return None

        return usr

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'email': self.email,
            'mobile': self.mobile,
            'lat_long': self.lat_long,
            'role': self.role,
            'user_id': self.user_id,
            'registration_key': self.registration_key
        }
