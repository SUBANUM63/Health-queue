from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from healthqueue.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from healthqueue.users.routes import users
    from healthqueue.queues.routes import queues
    from healthqueue.main.routes import main
    from healthqueue.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(queues)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
