from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'apieuab920iwehfo'

    from .views import home_page, tables, selection_1, unloading, loading, notes

    app.register_blueprint(home_page, url_prefix = '/')
    app.register_blueprint(selection_1, url_prefix = '/home-selection')
    app.register_blueprint(tables, url_prefix = '/table')
    app.register_blueprint(unloading, url_prefix = '/unload')
    app.register_blueprint(loading, url_prefix = '/load')
    app.register_blueprint(notes, url_prefix = '/notes')

    return app