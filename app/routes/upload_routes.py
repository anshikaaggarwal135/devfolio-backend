import uuid

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.services.storage_service import (
    supabase,
    BUCKET_NAME,
    delete_profile_image
)

upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")


@upload_bp.route("/profile-image", methods=["POST"])
@jwt_required()
def upload_profile_image():
    if "image" not in request.files:
        return {"error": "No image provided"}, 400

    image = request.files["image"]

    if image.filename == "":
        return {"error": "No image selected"}, 400

    allowed_extensions = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }

    filename = image.filename
    extension = filename.rsplit(".", 1)[-1].lower()

    if extension not in allowed_extensions:
        return {
            "error": "Only JPG, JPEG, PNG and WEBP images are allowed"
        }, 400

    unique_filename = f"profile-{uuid.uuid4()}.{extension}"

    try:
        file_bytes = image.read()

        supabase.storage.from_(BUCKET_NAME).upload(
            unique_filename,
            file_bytes,
            {
                "content-type": image.content_type
            }
        )

        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(
            unique_filename
        )

        return {
            "message": "Profile image uploaded successfully",
            "image_url": public_url,
            "filename": unique_filename
        }, 201

    except Exception as error:
        print("Upload error:", error)

        return {
            "error": "Failed to upload profile image"
        }, 500