from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# initializing
app = Flask(__name__)
app.config.from_object(Config)



#registering plug ins
#init for database managment
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#login

login = LoginManager(app)


#configure some settings
login.login_view = 'login'
login.login_message = 'Log In first!'
login.login_message_category = 'warning'
from app import models

from.blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from.blueprints.main import bp as main_bp
app.register_blueprint(main_bp)