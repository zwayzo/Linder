from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from os import path
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
DB_NAME = "flaskdb"
mail = Mail()
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flaskuser:flaskpass@localhost:5432/flaskdb"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'medazzeddine48@gmail.com'
    app.config['MAIL_PASSWORD'] = 'skcsyrtcszytlasv '
    app.config['MAIL_DEFAULT_SENDER'] = 'medazzeddine48@gmail.com'
    mail.init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'

    # Import models before user_loader
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from .views import views
    from .auth import auth
    from .interest import interest
    # from .profile import profile
    from .user import user
    from .chat import chat
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(interest, url_prefix='/api/')
    app.register_blueprint(user, url_prefix='/api/users')
    app.register_blueprint(chat, url_prefix='/api/chat')
    create_database(app)

    return app


def create_database(app):
    """Create tables in PostgreSQL if they don't exist"""
    with app.app_context():
        db.create_all()
        print("Database tables created!")
