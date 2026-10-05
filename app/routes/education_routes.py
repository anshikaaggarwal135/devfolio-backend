from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Education


education_bp = Blueprint(
    "education",
    __name__,
    url_prefix="/api/education"
)


# GET all education
@education_bp.route("/", methods=["GET"])
def get_education():

    education = Education.query.order_by(
        Education.id.desc()
    ).all()

    return {
        "education": [
            {
                "id": item.id,
                "institution": item.institution,
                "degree": item.degree,
                "field_of_study": item.field_of_study,
                "description": item.description,
                "start_date": (
                    item.start_date.isoformat()
                    if item.start_date
                    else None
                ),
                "end_date": (
                    item.end_date.isoformat()
                    if item.end_date
                    else None
                )
            }
            for item in education
        ]
    }, 200


# GET single education
@education_bp.route("/<int:education_id>", methods=["GET"])
def get_single_education(education_id):

    item = db.session.get(
        Education,
        education_id
    )

    if not item:
        return {
            "error": "Education not found"
        }, 404

    return {
        "education": {
            "id": item.id,
            "institution": item.institution,
            "degree": item.degree,
            "field_of_study": item.field_of_study,
            "description": item.description,
            "start_date": (
                item.start_date.isoformat()
                if item.start_date
                else None
            ),
            "end_date": (
                item.end_date.isoformat()
                if item.end_date
                else None
            )
        }
    }, 200


# CREATE education
@education_bp.route("/", methods=["POST"])
@jwt_required()
def create_education():

    data = request.get_json()

    institution = data.get("institution")
    degree = data.get("degree")

    if not institution or not degree:
        return {
            "error": "Institution and degree are required"
        }, 400

    item = Education(
        institution=institution,
        degree=degree,
        field_of_study=data.get("field_of_study"),
        description=data.get("description"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date")
    )

    db.session.add(item)
    db.session.commit()

    return {
        "message": "Education created successfully",
        "education": {
            "id": item.id,
            "institution": item.institution,
            "degree": item.degree,
            "field_of_study": item.field_of_study,
            "description": item.description,
            "start_date": (
                item.start_date.isoformat()
                if item.start_date
                else None
            ),
            "end_date": (
                item.end_date.isoformat()
                if item.end_date
                else None
            )
        }
    }, 201


# UPDATE education
@education_bp.route("/<int:education_id>", methods=["PUT"])
@jwt_required()
def update_education(education_id):

    item = db.session.get(
        Education,
        education_id
    )

    if not item:
        return {
            "error": "Education not found"
        }, 404

    data = request.get_json()

    item.institution = data.get(
        "institution",
        item.institution
    )

    item.degree = data.get(
        "degree",
        item.degree
    )

    item.field_of_study = data.get(
        "field_of_study",
        item.field_of_study
    )

    item.description = data.get(
        "description",
        item.description
    )

    item.start_date = data.get(
        "start_date",
        item.start_date
    )

    item.end_date = data.get(
        "end_date",
        item.end_date
    )

    db.session.commit()

    return {
        "message": "Education updated successfully"
    }, 200


# DELETE education
@education_bp.route("/<int:education_id>", methods=["DELETE"])
@jwt_required()
def delete_education(education_id):

    item = db.session.get(
        Education,
        education_id
    )

    if not item:
        return {
            "error": "Education not found"
        }, 404

    db.session.delete(item)
    db.session.commit()

    return {
        "message": "Education deleted successfully"
    }, 200