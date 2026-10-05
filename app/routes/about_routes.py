from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import About


about_bp = Blueprint(
    "about",
    __name__,
    url_prefix="/api/about"
)


# GET About - Public
@about_bp.route("/", methods=["GET"])
def get_about():

    about = About.query.first()

    if not about:
        return {
            "about": None
        }, 200

    return {
        "about": {
            "id": about.id,
            "title": about.title,
            "content": about.content,
            "profile_image_url": about.profile_image_url,
            "resume_url": about.resume_url,
            "updated_at": (
                about.updated_at.isoformat()
                if about.updated_at
                else None
            )
        }
    }, 200


# CREATE About - Admin
@about_bp.route("/", methods=["POST"])
@jwt_required()
def create_about():

    existing = About.query.first()

    if existing:
        return {
            "error": "About section already exists"
        }, 409

    data = request.get_json() or {}

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return {
            "error": "Title and content are required"
        }, 400

    about = About(
        title=title,
        content=content,
        profile_image_url=data.get("profile_image_url"),
        resume_url=data.get("resume_url")
    )

    db.session.add(about)
    db.session.commit()

    return {
        "message": "About section created successfully"
    }, 201


# UPDATE About - Admin
@about_bp.route("/", methods=["PUT"])
@jwt_required()
def update_about():

    about = About.query.first()

    if not about:
        return {
            "error": "About section not found"
        }, 404

    data = request.get_json() or {}

    about.title = data.get(
        "title",
        about.title
    )

    about.content = data.get(
        "content",
        about.content
    )

    about.profile_image_url = data.get(
        "profile_image_url",
        about.profile_image_url
    )

    about.resume_url = data.get(
        "resume_url",
        about.resume_url
    )

    db.session.commit()

    return {
        "message": "About section updated successfully"
    }, 200