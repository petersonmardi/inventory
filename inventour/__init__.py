from flask import Flask
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.urandom(32),
        DATABASE=os.path.join(app.instance_path,"inventory.sqlite"),
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    from .routes.auth import auth
    app.register_blueprint(auth.bp)
    
    from .routes import index
    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")

    return app
