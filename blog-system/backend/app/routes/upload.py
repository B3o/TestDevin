from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import uuid
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "static/uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename using UUID and timestamp."""
    extension = get_file_extension(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}-{unique_id}{extension}"

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file."""
    # Validate file extension
    extension = get_file_extension(file.filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Save the file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Return the URL
        return {
            "url": f"/static/uploads/{filename}",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
