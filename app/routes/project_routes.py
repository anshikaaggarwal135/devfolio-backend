from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Project


project_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/api/projects"
)


# GET all projects
@project_bp.route("/", methods=["GET"])
def get_projects():

    projects = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    return {
        "projects": [
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "technologies": project.technologies,
                "github_url": project.github_url,
                "live_url": project.live_url,
                "image_url": project.image_url
            }
            for project in projects
        ]
    }, 200


# GET single project
@project_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        return {
            "error": "Project not found"
        }, 404

    return {
        "project": {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "technologies": project.technologies,
            "github_url": project.github_url,
            "live_url": project.live_url,
            "image_url": project.image_url
        }
    }, 200


# CREATE project
@project_bp.route("/", methods=["POST"])
@jwt_required()
def create_project():

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return {
            "error": "Title and description are required"
        }, 400

    project = Project(
        title=title,
        description=description,
        technologies=data.get("technologies"),
        github_url=data.get("github_url"),
        live_url=data.get("live_url"),
        image_url=data.get("image_url")
    )

    db.session.add(project)
    db.session.commit()

    return {
        "message": "Project created successfully",
        "project": {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "technologies": project.technologies,
            "github_url": project.github_url,
            "live_url": project.live_url,
            "image_url": project.image_url
        }
    }, 201


# UPDATE project
@project_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        return {
            "error": "Project not found"
        }, 404

    data = request.get_json()

    project.title = data.get("title", project.title)
    project.description = data.get(
        "description",
        project.description
    )
    project.technologies = data.get(
        "technologies",
        project.technologies
    )
    project.github_url = data.get(
        "github_url",
        project.github_url
    )
    project.live_url = data.get(
        "live_url",
        project.live_url
    )
    project.image_url = data.get(
        "image_url",
        project.image_url
    )

    db.session.commit()

    return {
        "message": "Project updated successfully"
    }, 200


# DELETE project
@project_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        return {
            "error": "Project not found"
        }, 404

    db.session.delete(project)
    db.session.commit()

    return {
        "message": "Project deleted successfully"
    }, 200