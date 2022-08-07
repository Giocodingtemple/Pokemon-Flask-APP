from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# initializing
app = Flask(__name__)
app.config.from_object(Config)

## Registering plugin/exts

# init for database management
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login
login = LoginManager(app)

# Configure some Settings
login.login_view = 'login'
login.login_message = 'Log yourself in or your fired'
login.login_message_category = 'warning'

from.blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from.blueprints.pokemon import bp as pokemon_bp
app.register_blueprint(pokemon_bp)

from app import models
