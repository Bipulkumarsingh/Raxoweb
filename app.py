from flask import Flask
from flask_restful import Resource, Api
from resources.user import UserRegister, UserLogin, UserLogout, TokenRefresh
from flask_jwt_extended import JWTManager
from resources.validate import (AuthUser, ResendOtp, ResetPassword, GenerateReset,
                                ValidateReset)
from resources.contact import ContactUs
from flask_cors import CORS
from db import db
from resources.article import UserPost
from blacklist import BLACKLIST
from appoptics_apm.middleware import AppOpticsApmMiddleware
app = Flask(__name__)
app.wsgi_app = AppOpticsApmMiddleware(app.wsgi_app)
CORS(app)
api = Api(app)

environment = 'dev'
if environment == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
    app.debug = True

    @app.before_first_request
    def create_tables():
        db.create_all()
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://...'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
# app.config['SECRET_KEY'] = '_ra/xo$web!@secret#key_'
app.secret_key = "_create_any_code_with_special_character_"  # could do app.config['JWT_SECRET_KEY'] if we prefer

db.init_app(app)
app.app_context().push()

jwt = JWTManager(app)


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


class Home(Resource):
    @staticmethod
    def get():
        return {"status": "success 200"}

    @staticmethod
    def post():
        return {"status": "success 200"}


api.add_resource(Home, '/')
api.add_resource(UserRegister, '/register')
api.add_resource(AuthUser, '/validate')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, "/refresh")
# resource_class_kwargs={'secret': app.config['SECRET_KEY']})
api.add_resource(ContactUs, '/contact-us')
api.add_resource(ResendOtp, '/resend-otp')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(GenerateReset, '/forgot-password/<string:otp>')
api.add_resource(ValidateReset, '/change-password')
api.add_resource(UserPost, '/blog-post')
# resource_class_kwargs={'secret': app.config['SECRET_KEY']})
if __name__ == '__main__':
    app.run()
