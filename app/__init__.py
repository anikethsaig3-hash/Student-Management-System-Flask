from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy (db) here so models can import it
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = 'dev'  # change in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Import routes and models so they are registered with the app
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

        return app
