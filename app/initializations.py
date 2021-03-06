import pymysql
from flask import Flask
from flask_restplus import Api, fields
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Help Your Neighbor",
          description="Help Your Neighbor application"
          )

pymysql.install_as_MySQLdb()

# flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/db'

db = SQLAlchemy(flask_app)

name_space = app.namespace('help_your_neighbor', description='Help Your Neighbor APIs')

Person = app.model('Person Model',
                   {'first_name': fields.String(required=True,
                                                description="First Name",
                                                help="First Name cannot be blank"),

                    'last_name': fields.String(required=True,
                                               description="Last Name",
                                               help="Last Name cannot be blank"),

                    'address': fields.String(required=False,
                                             description="Address",
                                             help=""),

                    'email': fields.String(required=False,
                                           description="Email",
                                           help=""),

                    'mobile': fields.String(required=False,
                                            description="Mobile",
                                            help=""),

                    'lat_long': fields.String(required=False,
                                              description="Latitude, Longitude",
                                              help=""),

                    'role': fields.String(required=True,
                                          description="Role should be one of the following [Admin, Donor, Needy]",
                                          help="Role should be one of the following [Admin, Donor, Needy]"),

                    })

Auth = app.model('Auth Model',
                 {'username': fields.String(required=True,
                                            description="Username",
                                            help="Username cannot be blank"),

                  'password': fields.String(required=True,
                                            description="It is highly unsafe to send passwords directly. Send SHA-256 of password.",
                                            help="Password cannot be blank")
                  })

Dashboard = app.model('Dashboard Model',
                      {'token': fields.String(required=True,
                                              description="access_token",
                                              help="access_token cannot be blank")
                       })

Registration = app.model('Register Model',
                         {'username': fields.String(required=True,
                                                    description="Username",
                                                    help="Username cannot be blank"),

                          'password': fields.String(required=True,
                                                    description="It is highly unsafe to send passwords directly. Send SHA-256 of password.",
                                                    help="Password cannot be blank")
                          })

Help = app.model('Help Model',
                 {'description': fields.String(required=False,
                                               description="description",
                                               help="description cannot be blank"),

                  'note': fields.String(required=True,
                                         description="note",
                                         help="note"),
                  'address': fields.String(required=False,
                                           description="Address",
                                           help=""),
                  'location': fields.String(required=False,
                                            description="Latitude, Longitude",
                                            help=""),
                  'token': fields.String(required=True,
                                         description="token",
                                         help=""),
                  'closed': fields.Boolean(required=False,
                                           description="Should this be closed?",
                                           help="", default=False)

                  })
