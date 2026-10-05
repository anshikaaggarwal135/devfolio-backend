import os

from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)

BUCKET_NAME = "profile-images"


def delete_profile_image(image_url):
    """
    Delete an old profile image from Supabase Storage.
    """

    if not image_url:
        return False

    try:
        marker = f"/storage/v1/object/public/{BUCKET_NAME}/"

        if marker not in image_url:
            print("Could not determine old image path.")
            print("Image URL:", image_url)
            return False

        file_path = image_url.split(marker, 1)[1]

        print("Deleting old profile image:", file_path)

        result = supabase.storage.from_(BUCKET_NAME).remove([
            file_path
        ])

        print("Supabase delete result:", result)

        return True

    except Exception as error:
        print("Failed to delete old profile image:", error)
        return False