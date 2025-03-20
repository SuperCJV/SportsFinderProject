#set up flask file
from flask import Flask

#for the database
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#object for database
db = SQLAlchemy()
DB_NAME = "database.db"

#define app
def create_app():
    app = Flask(__name__)
    #encrypt session data for website
    app.config['SECRET_KEY'] = 'cen4090l'

    #tell flask that we are going to be using the database and where it is located
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    #initialize database
    db.init_app(app)

    #register blueprints from views and auth
    from .views import views
    from .auth import auth

    #register them for our applications
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')