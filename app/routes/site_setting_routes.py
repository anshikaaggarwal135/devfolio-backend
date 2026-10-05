from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import SiteSetting


site_setting_bp = Blueprint(
    "site_settings",
    __name__,
    url_prefix="/api/site-settings"
)


# GET site settings - Public
@site_setting_bp.route("/", methods=["GET"])
def get_site_settings():

    settings = SiteSetting.query.first()

    if not settings:
        return {
            "site_settings": None
        }, 200

    return {
        "site_settings": {
            "id": settings.id,
            "site_name": settings.site_name,
            "email": settings.email,
            "phone": settings.phone,
            "location": settings.location,
            "favicon_url": settings.favicon_url,
            "updated_at": (
                settings.updated_at.isoformat()
                if settings.updated_at
                else None
            )
        }
    }, 200


# CREATE site settings - Admin
@site_setting_bp.route("/", methods=["POST"])
@jwt_required()
def create_site_settings():

    existing = SiteSetting.query.first()

    if existing:
        return {
            "error": "Site settings already exist"
        }, 409

    data = request.get_json() or {}

    site_name = data.get("site_name")

    if not site_name:
        return {
            "error": "Site name is required"
        }, 400

    settings = SiteSetting(
        site_name=site_name,
        email=data.get("email"),
        phone=data.get("phone"),
        location=data.get("location"),
        favicon_url=data.get("favicon_url")
    )

    db.session.add(settings)
    db.session.commit()

    return {
        "message": "Site settings created successfully"
    }, 201


# UPDATE site settings - Admin
@site_setting_bp.route("/", methods=["PUT"])
@jwt_required()
def update_site_settings():

    settings = SiteSetting.query.first()

    if not settings:
        return {
            "error": "Site settings not found"
        }, 404

    data = request.get_json() or {}

    settings.site_name = data.get(
        "site_name",
        settings.site_name
    )

    settings.email = data.get(
        "email",
        settings.email
    )

    settings.phone = data.get(
        "phone",
        settings.phone
    )

    settings.location = data.get(
        "location",
        settings.location
    )

    settings.favicon_url = data.get(
        "favicon_url",
        settings.favicon_url
    )

    db.session.commit()

    return {
        "message": "Site settings updated successfully"
    }, 200