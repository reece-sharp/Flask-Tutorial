import os

from flask import Flask
import os

from flask import Flask
 # this creates the application

def create_app(test_config=None):  # def is the syntax to create a function
    # create and configure the app
    # create_app is the application factory function. You’ll add to it later in the tutorial, but it already does a lot.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # SECRET_KEY: is used by Flask and extensions to keep data safe.
        # SECRET_KEY: Its set to 'dev' to provide a convenient value during development
        # SECRET_KEY: but it should be overridden with a random value when deploying
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # this is where my database is stored
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        # os.makedirs() ensures that app.instance_path exists.
        # Flask doesn’t create the instance folder automatically,
        # but it needs to be created because your project will create the SQLite database file there.
    except OSError:
        pass




# lines 45-46 were added from teh Define and Access the Database section
    from . import db # import the db.py script
    db.init_app(app) # making it possible to use the db script with the flask applictaion
    # this ^ IS the app and before it wasn't in teh create app f() so it didnt show up

    from . import auth
    app.register_blueprint(auth.bp)

    from . import library
    app.register_blueprint(library.bp)
    app.add_url_rule('/', endpoint='index')

    return app
    # return need to be indented to be a part of the f()


