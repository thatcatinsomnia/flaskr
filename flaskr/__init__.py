import os
from flask import Flask

def create_app(test_config=None):
    # create flask instance
    app = Flask(__name__, instance_relative_config=True)

    # secret key should overridden with random value when deploying
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    
    if test_config is None:
        # load the instance config, if it exist
        app.config.from_pyfile('config.py', silent=True)    # set secret in the config.py
    else:
        # load the test config if not test
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # flask doesn't create the folder automatically, need to becreated
    try:
        os.makedirs(app.instance_path)  
    except OSError:
        pass

    # a simple page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # import and call the db.py function
    from . import db
    db.init_app(app)

    # register auth
    from . import auth
    app.register_blueprint(auth.bp)
    
    # register blog, url_for('index') or url_for('blog.index') will both work
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
