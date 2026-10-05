from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Skill


skill_bp = Blueprint(
    "skills",
    __name__,
    url_prefix="/api/skills"
)


# GET all skills
@skill_bp.route("/", methods=["GET"])
def get_skills():

    skills = Skill.query.order_by(
        Skill.id.asc()
    ).all()

    return {
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "category": skill.category
            }
            for skill in skills
        ]
    }, 200


# GET single skill
@skill_bp.route("/<int:skill_id>", methods=["GET"])
def get_skill(skill_id):

    skill = db.session.get(Skill, skill_id)

    if not skill:
        return {
            "error": "Skill not found"
        }, 404

    return {
        "skill": {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category
        }
    }, 200


# CREATE skill
@skill_bp.route("/", methods=["POST"])
@jwt_required()
def create_skill():

    data = request.get_json()

    name = data.get("name")
    category = data.get("category")

    if not name:
        return {
            "error": "Skill name is required"
        }, 400

    skill = Skill(
        name=name,
        category=category
    )

    db.session.add(skill)
    db.session.commit()

    return {
        "message": "Skill created successfully",
        "skill": {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category
        }
    }, 201


# UPDATE skill
@skill_bp.route("/<int:skill_id>", methods=["PUT"])
@jwt_required()
def update_skill(skill_id):

    skill = db.session.get(Skill, skill_id)

    if not skill:
        return {
            "error": "Skill not found"
        }, 404

    data = request.get_json()

    skill.name = data.get("name", skill.name)
    skill.category = data.get("category", skill.category)

    db.session.commit()

    return {
        "message": "Skill updated successfully"
    }, 200


# DELETE skill
@skill_bp.route("/<int:skill_id>", methods=["DELETE"])
@jwt_required()
def delete_skill(skill_id):

    skill = db.session.get(Skill, skill_id)

    if not skill:
        return {
            "error": "Skill not found"
        }, 404

    db.session.delete(skill)
    db.session.commit()

    return {
        "message": "Skill deleted successfully"
    }, 200