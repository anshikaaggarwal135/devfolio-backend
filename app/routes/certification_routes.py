from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Certification


certification_bp = Blueprint(
    "certifications",
    __name__,
    url_prefix="/api/certifications"
)


# GET all certifications
@certification_bp.route("/", methods=["GET"])
def get_certifications():

    certifications = Certification.query.order_by(
        Certification.id.desc()
    ).all()

    return {
        "certifications": [
            {
                "id": item.id,
                "title": item.title,
                "issuer": item.issuer,
                "description": item.description,
                "issue_date": (
                    item.issue_date.isoformat()
                    if item.issue_date
                    else None
                ),
                "credential_url": item.credential_url
            }
            for item in certifications
        ]
    }, 200


# GET single certification
@certification_bp.route("/<int:certification_id>", methods=["GET"])
def get_certification(certification_id):

    item = db.session.get(
        Certification,
        certification_id
    )

    if not item:
        return {
            "error": "Certification not found"
        }, 404

    return {
        "certification": {
            "id": item.id,
            "title": item.title,
            "issuer": item.issuer,
            "description": item.description,
            "issue_date": (
                item.issue_date.isoformat()
                if item.issue_date
                else None
            ),
            "credential_url": item.credential_url
        }
    }, 200


# CREATE certification
@certification_bp.route("/", methods=["POST"])
@jwt_required()
def create_certification():

    data = request.get_json()

    title = data.get("title")
    issuer = data.get("issuer")

    if not title or not issuer:
        return {
            "error": "Title and issuer are required"
        }, 400

    item = Certification(
        title=title,
        issuer=issuer,
        description=data.get("description"),
        issue_date=data.get("issue_date") or None,
        credential_url=data.get("credential_url")
    )

    db.session.add(item)
    db.session.commit()

    return {
        "message": "Certification created successfully",
        "certification": {
            "id": item.id,
            "title": item.title,
            "issuer": item.issuer,
            "description": item.description,
            "issue_date": (
                item.issue_date.isoformat()
                if item.issue_date
                else None
            ),
            "credential_url": item.credential_url
        }
    }, 201


# UPDATE certification
@certification_bp.route("/<int:certification_id>", methods=["PUT"])
@jwt_required()
def update_certification(certification_id):

    item = db.session.get(
        Certification,
        certification_id
    )

    if not item:
        return {
            "error": "Certification not found"
        }, 404

    data = request.get_json()

    item.title = data.get(
        "title",
        item.title
    )

    item.issuer = data.get(
        "issuer",
        item.issuer
    )

    item.description = data.get(
        "description",
        item.description
    )

    item.issue_date = data.get(
        "issue_date",
        item.issue_date
    )

    item.credential_url = data.get(
        "credential_url",
        item.credential_url
    )

    db.session.commit()

    return {
        "message": "Certification updated successfully"
    }, 200


# DELETE certification
@certification_bp.route("/<int:certification_id>", methods=["DELETE"])
@jwt_required()
def delete_certification(certification_id):

    item = db.session.get(
        Certification,
        certification_id
    )

    if not item:
        return {
            "error": "Certification not found"
        }, 404

    db.session.delete(item)
    db.session.commit()

    return {
        "message": "Certification deleted successfully"
    }, 200