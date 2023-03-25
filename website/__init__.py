from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'apieuab920iwehfo'

    from .views import home_page, tables, selection_1, unloading, loading, notes, logs, select_log

    app.register_blueprint(home_page, url_prefix = '/')
    app.register_blueprint(selection_1, url_prefix = '/home-selection')
    app.register_blueprint(tables, url_prefix = '/table')
    app.register_blueprint(unloading, url_prefix = '/unload')
    app.register_blueprint(loading, url_prefix = '/load')
    app.register_blueprint(notes, url_prefix = '/notes')
    app.register_blueprint(logs, url_prefix = '/log')
    app.register_blueprint(select_log, url_prefix = '/log_select')
    

    return app