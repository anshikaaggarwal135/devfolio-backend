from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # CORS configuration
    CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost:5174",
                "https://devfolio-cms-tau.vercel.app"
            ]
        }
    }
)
    
    
    @app.route("/")
    def home():
        return {"message": "Devfolio Backend is running"}

    from app.models import (
        User,
        Project,
        Skill,
        Experience,
        Education,
        Certification,
        Message,
        About,
        Hero,
        SocialLink,
        SiteSetting
    )

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.project_routes import project_bp
    app.register_blueprint(project_bp)

    from app.routes.skill_routes import skill_bp
    app.register_blueprint(skill_bp)

    from app.routes.experience_routes import experience_bp
    app.register_blueprint(experience_bp)

    from app.routes.education_routes import education_bp
    app.register_blueprint(education_bp)

    from app.routes.certification_routes import certification_bp
    app.register_blueprint(certification_bp)

    from app.routes.message_routes import message_bp
    app.register_blueprint(message_bp)

    from app.routes.about_routes import about_bp
    app.register_blueprint(about_bp)

    from app.routes.hero_routes import hero_bp
    app.register_blueprint(hero_bp)

    from app.routes.social_routes import social_bp
    app.register_blueprint(social_bp)

    from app.routes.site_setting_routes import site_setting_bp
    app.register_blueprint(site_setting_bp)

    from app.routes.upload_routes import upload_bp
    app.register_blueprint(upload_bp)

    return app