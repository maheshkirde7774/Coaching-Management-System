from flask import Flask, render_template
from config import Config
from models import db
from models.user import User
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.public import public_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.students import students_bp
    from routes.admissions import admissions_bp
    from routes.attendance import attendance_bp
    from routes.fees import fees_bp
    from routes.notices import notices_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(students_bp, url_prefix='/admin/students')
    app.register_blueprint(admissions_bp, url_prefix='/admin/admissions')
    app.register_blueprint(attendance_bp, url_prefix='/admin/attendance')
    app.register_blueprint(fees_bp, url_prefix='/admin/fees')
    app.register_blueprint(notices_bp, url_prefix='/admin/notices')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
