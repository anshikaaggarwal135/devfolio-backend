from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import SocialLink


social_bp = Blueprint(
    "social",
    __name__,
    url_prefix="/api/social-links"
)


# GET all social links - Public
@social_bp.route("/", methods=["GET"])
def get_social_links():

    links = SocialLink.query.order_by(
        SocialLink.display_order.asc()
    ).all()

    return {
        "social_links": [
            {
                "id": link.id,
                "platform": link.platform,
                "url": link.url,
                "is_active": link.is_active,
                "display_order": link.display_order
            }
            for link in links
        ]
    }, 200


# GET single social link - Public
@social_bp.route("/<int:link_id>", methods=["GET"])
def get_social_link(link_id):

    link = db.session.get(
        SocialLink,
        link_id
    )

    if not link:
        return {
            "error": "Social link not found"
        }, 404

    return {
        "social_link": {
            "id": link.id,
            "platform": link.platform,
            "url": link.url,
            "is_active": link.is_active,
            "display_order": link.display_order
        }
    }, 200


# CREATE social link - Admin
@social_bp.route("/", methods=["POST"])
@jwt_required()
def create_social_link():

    data = request.get_json() or {}

    platform = data.get("platform")
    url = data.get("url")

    if not platform or not url:
        return {
            "error": "Platform and URL are required"
        }, 400

    link = SocialLink(
        platform=platform,
        url=url,
        is_active=data.get(
            "is_active",
            True
        ),
        display_order=data.get(
            "display_order",
            0
        )
    )

    db.session.add(link)
    db.session.commit()

    return {
        "message": "Social link created successfully"
    }, 201


# UPDATE social link - Admin
@social_bp.route("/<int:link_id>", methods=["PUT"])
@jwt_required()
def update_social_link(link_id):

    link = db.session.get(
        SocialLink,
        link_id
    )

    if not link:
        return {
            "error": "Social link not found"
        }, 404

    data = request.get_json() or {}

    link.platform = data.get(
        "platform",
        link.platform
    )

    link.url = data.get(
        "url",
        link.url
    )

    link.is_active = data.get(
        "is_active",
        link.is_active
    )

    link.display_order = data.get(
        "display_order",
        link.display_order
    )

    db.session.commit()

    return {
        "message": "Social link updated successfully"
    }, 200


# DELETE social link - Admin
@social_bp.route("/<int:link_id>", methods=["DELETE"])
@jwt_required()
def delete_social_link(link_id):

    link = db.session.get(
        SocialLink,
        link_id
    )

    if not link:
        return {
            "error": "Social link not found"
        }, 404

    db.session.delete(link)
    db.session.commit()

    return {
        "message": "Social link deleted successfully"
    }, 200