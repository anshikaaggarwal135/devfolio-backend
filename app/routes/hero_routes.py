from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.storage_service import delete_profile_image
from app import db
from app.models import Hero


hero_bp = Blueprint(
    "hero",
    __name__,
    url_prefix="/api/hero"
)


# GET hero - Public
@hero_bp.route("/", methods=["GET"])
def get_hero():

    hero = Hero.query.first()

    if not hero:
        return {
            "hero": None
        }, 200

    return {
        "hero": {
            "id": hero.id,
            "greeting": hero.greeting,
            "name": hero.name,
            "title": hero.title,
            "subtitle": hero.subtitle,
            "profile_image_url": hero.profile_image_url,
            "primary_button_text": hero.primary_button_text,
            "primary_button_url": hero.primary_button_url,
            "secondary_button_text": hero.secondary_button_text,
            "secondary_button_url": hero.secondary_button_url,
            "updated_at": (
                hero.updated_at.isoformat()
                if hero.updated_at
                else None
            )
        }
    }, 200


# CREATE hero - Admin
@hero_bp.route("/", methods=["POST"])
@jwt_required()
def create_hero():

    existing = Hero.query.first()

    if existing:
        return {
            "error": "Hero section already exists"
        }, 409

    data = request.get_json() or {}

    name = data.get("name")
    title = data.get("title")

    if not name or not title:
        return {
            "error": "Name and title are required"
        }, 400

    hero = Hero(
        greeting=data.get(
            "greeting",
            "Hi, I'm"
        ),
        name=name,
        title=title,
        subtitle=data.get("subtitle"),
        profile_image_url=data.get("profile_image_url"),
        primary_button_text=data.get(
            "primary_button_text",
            "View Projects"
        ),
        primary_button_url=data.get(
            "primary_button_url"
        ),
        secondary_button_text=data.get(
            "secondary_button_text",
            "Contact Me"
        ),
        secondary_button_url=data.get(
            "secondary_button_url"
        )
    )

    db.session.add(hero)
    db.session.commit()

    return {
        "message": "Hero section created successfully"
    }, 201


# UPDATE hero - Admin
@hero_bp.route("/", methods=["PUT"])
@jwt_required()
def update_hero():

    hero = Hero.query.first()

    if not hero:
        return {
            "error": "Hero section not found"
        }, 404

    data = request.get_json() or {}

    hero.greeting = data.get(
        "greeting",
        hero.greeting
    )

    hero.name = data.get(
        "name",
        hero.name
    )

    hero.title = data.get(
        "title",
        hero.title
    )

    hero.subtitle = data.get(
        "subtitle",
        hero.subtitle
    )

    hero.profile_image_url = data.get(
        "profile_image_url",
        hero.profile_image_url
    )

    hero.primary_button_text = data.get(
        "primary_button_text",
        hero.primary_button_text
    )

    hero.primary_button_url = data.get(
        "primary_button_url",
        hero.primary_button_url
    )

    hero.secondary_button_text = data.get(
        "secondary_button_text",
        hero.secondary_button_text
    )

    hero.secondary_button_url = data.get(
        "secondary_button_url",
        hero.secondary_button_url
    )

    db.session.commit()

    return {
        "message": "Hero section updated successfully"
    }, 200
    
# UPDATE profile image URL - Admin
@hero_bp.route("/profile-image", methods=["PUT"])
@jwt_required()
def update_profile_image():
    hero = Hero.query.first()

    if not hero:
        return {"error": "Hero section not found"}, 404

    data = request.get_json() or {}
    image_url = data.get("image_url")

    if not image_url:
        return {"error": "image_url is required"}, 400

    old_image_url = hero.profile_image_url

    hero.profile_image_url = image_url

    try:
        db.session.commit()

        # Delete the old image only after the new URL
        # has been successfully saved.
        if old_image_url and old_image_url != image_url:
            delete_profile_image(old_image_url)

        return {
            "message": "Profile image URL updated successfully",
            "image_url": hero.profile_image_url
        }, 200

    except Exception as error:
        db.session.rollback()

        print("Profile image update error:", error)

        return {
            "error": "Failed to update profile image"
        }, 500