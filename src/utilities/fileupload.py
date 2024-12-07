import aiofiles
import secrets
from pathlib import Path
from PIL import Image
import os
from fastapi import HTTPException, UploadFile, status

UPLOAD_DIR = Path("../static/images")

# Ensure the directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_file(file: UploadFile) -> str:
    valid_extensions = ["png", "jpg", "jpeg"]
    filename = file.filename
    extension = filename.split(".")[-1].lower()

    if extension not in valid_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a PNG, JPG, or JPEG image.",
        )

    # Generate a secure filename
    token_name = f"{secrets.token_hex(10)}.{extension}"
    file_path = UPLOAD_DIR / token_name

    # Save the file asynchronously
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024):
                await f.write(chunk)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save the file: {str(e)}",
        )

    # Resize the image while maintaining aspect ratio
    try:
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize while maintaining aspect ratio
        img.save(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process the image: {str(e)}",
        )

    return token_name


def delete_file(filename: str):
    """
    Delete an existing file if it exists.

    Args:
        filename (str): The filename to be deleted.
    """
    file_path = UPLOAD_DIR / filename
    try:
        if file_path.exists():
            os.remove(file_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {filename} not found.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete the file: {str(e)}",
        )
