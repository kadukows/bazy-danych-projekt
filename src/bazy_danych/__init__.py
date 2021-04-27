from flask import Flask, render_template
from flask_login import current_user

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    from . import db
    db.init_app(app)

    from flask_bootstrap import Bootstrap
    bootstrap = Bootstrap(app)

    from . import routes
    routes.init_app(app)

    from . import auth
    auth.init_app(app)

    return app
