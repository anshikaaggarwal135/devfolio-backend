from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app import db
from app.models import Message


message_bp = Blueprint(
    "messages",
    __name__,
    url_prefix="/api/messages"
)


# CREATE message - Public
@message_bp.route("/", methods=["POST"])
def create_message():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message_text = data.get("message")

    if not name or not email or not message_text:
        return {
            "error": "Name, email and message are required"
        }, 400

    message = Message(
        name=name,
        email=email,
        subject=data.get("subject"),
        message=message_text
    )

    db.session.add(message)
    db.session.commit()

    return {
        "message": "Message sent successfully"
    }, 201


# GET all messages - Admin
@message_bp.route("/", methods=["GET"])
@jwt_required()
def get_messages():

    messages = Message.query.order_by(
        Message.created_at.desc()
    ).all()

    return {
        "messages": [
            {
                "id": item.id,
                "name": item.name,
                "email": item.email,
                "subject": item.subject,
                "message": item.message,
                "is_read": item.is_read,
                "created_at": (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                )
            }
            for item in messages
        ]
    }, 200


# GET single message - Admin
@message_bp.route("/<int:message_id>", methods=["GET"])
@jwt_required()
def get_message(message_id):

    item = db.session.get(
        Message,
        message_id
    )

    if not item:
        return {
            "error": "Message not found"
        }, 404

    return {
        "message": {
            "id": item.id,
            "name": item.name,
            "email": item.email,
            "subject": item.subject,
            "message": item.message,
            "is_read": item.is_read,
            "created_at": (
                item.created_at.isoformat()
                if item.created_at
                else None
            )
        }
    }, 200


# MARK MESSAGE AS READ - Admin
@message_bp.route("/<int:message_id>/read", methods=["PUT"])
@jwt_required()
def mark_message_read(message_id):

    item = db.session.get(
        Message,
        message_id
    )

    if not item:
        return {
            "error": "Message not found"
        }, 404

    item.is_read = True

    db.session.commit()

    return {
        "message": "Message marked as read"
    }, 200


# DELETE message - Admin
@message_bp.route("/<int:message_id>", methods=["DELETE"])
@jwt_required()
def delete_message(message_id):

    item = db.session.get(
        Message,
        message_id
    )

    if not item:
        return {
            "error": "Message not found"
        }, 404

    db.session.delete(item)
    db.session.commit()

    return {
        "message": "Message deleted successfully"
    }, 200