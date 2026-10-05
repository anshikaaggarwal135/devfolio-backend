from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Experience


experience_bp = Blueprint(
    "experiences",
    __name__,
    url_prefix="/api/experiences"
)


# GET all experiences
@experience_bp.route("/", methods=["GET"])
def get_experiences():

    experiences = Experience.query.order_by(
        Experience.id.desc()
    ).all()

    return {
        "experiences": [
            {
                "id": experience.id,
                "company": experience.company,
                "role": experience.role,
                "description": experience.description,
                "start_date": (
                    experience.start_date.isoformat()
                    if experience.start_date
                    else None
                ),
                "end_date": (
                    experience.end_date.isoformat()
                    if experience.end_date
                    else None
                ),
                "technologies": experience.technologies
            }
            for experience in experiences
        ]
    }, 200


# GET single experience
@experience_bp.route("/<int:experience_id>", methods=["GET"])
def get_experience(experience_id):

    experience = db.session.get(
        Experience,
        experience_id
    )

    if not experience:
        return {
            "error": "Experience not found"
        }, 404

    return {
        "experience": {
            "id": experience.id,
            "company": experience.company,
            "role": experience.role,
            "description": experience.description,
            "start_date": (
                experience.start_date.isoformat()
                if experience.start_date
                else None
            ),
            "end_date": (
                experience.end_date.isoformat()
                if experience.end_date
                else None
            ),
            "technologies": experience.technologies
        }
    }, 200


# CREATE experience
@experience_bp.route("/", methods=["POST"])
@jwt_required()
def create_experience():

    data = request.get_json()

    company = data.get("company")
    role = data.get("role")

    if not company or not role:
        return {
            "error": "Company and role are required"
        }, 400

    experience = Experience(
        company=company,
        role=role,
        description=data.get("description"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        technologies=data.get("technologies")
    )

    db.session.add(experience)
    db.session.commit()

    return {
        "message": "Experience created successfully",
        "experience": {
            "id": experience.id,
            "company": experience.company,
            "role": experience.role,
            "description": experience.description,
            "start_date": (
                experience.start_date.isoformat()
                if experience.start_date
                else None
            ),
            "end_date": (
                experience.end_date.isoformat()
                if experience.end_date
                else None
            ),
            "technologies": experience.technologies
        }
    }, 201


# UPDATE experience
@experience_bp.route("/<int:experience_id>", methods=["PUT"])
@jwt_required()
def update_experience(experience_id):

    experience = db.session.get(
        Experience,
        experience_id
    )

    if not experience:
        return {
            "error": "Experience not found"
        }, 404

    data = request.get_json()

    experience.company = data.get(
        "company",
        experience.company
    )

    experience.role = data.get(
        "role",
        experience.role
    )

    experience.description = data.get(
        "description",
        experience.description
    )

    experience.start_date = data.get(
        "start_date",
        experience.start_date
    )

    experience.end_date = data.get(
        "end_date",
        experience.end_date
    )

    experience.technologies = data.get(
        "technologies",
        experience.technologies
    )

    db.session.commit()

    return {
        "message": "Experience updated successfully"
    }, 200


# DELETE experience
@experience_bp.route("/<int:experience_id>", methods=["DELETE"])
@jwt_required()
def delete_experience(experience_id):

    experience = db.session.get(
        Experience,
        experience_id
    )

    if not experience:
        return {
            "error": "Experience not found"
        }, 404

    db.session.delete(experience)
    db.session.commit()

    return {
        "message": "Experience deleted successfully"
    }, 200