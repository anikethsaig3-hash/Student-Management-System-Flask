from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy (db) here so models can import it
# db is a module-level object so other modules can `from app import db`
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = 'dev'  # change in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Import routes and models so they are registered with the app
        # routes uses `current_app` as `app` and must be imported inside an app context
        from . import routes, models  # noqa: F401
        db.create_all()

        # Register error handlers
        @app.errorhandler(404)
        def not_found(error):
            from flask import render_template
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def server_error(error):
            from flask import render_template
            return render_template('500.html'), 500

    # Try to register API blueprint (api.py is a top-level module)
    try:
        # Import here to avoid circular import problems during package import
        import api
        if hasattr(api, 'api_bp'):
            app.register_blueprint(api.api_bp, url_prefix='/api')
    except Exception:
        # If api.py is missing or has errors, do not break the main app
        app.logger.debug('api blueprint not registered: api module not available')

    return app
