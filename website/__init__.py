from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'apieuab920iwehfo'

    from .views import home_page, tables

    app.register_blueprint(home_page, url_prefix = '/')
    app.register_blueprint(tables, url_prefix = '/table')

    return app