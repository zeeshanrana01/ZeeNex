from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/images", tags=["images"])

UPLOAD_DIR = Path("api/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Mount the uploads directory to serve images publicly
# Note: In a production app, you'd handle this in main.py,
# but for now we provide the route and assume static mounting.

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_extension = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    # In a real app, this would be a full URL to S3 or a CDN
    # For local dev, we return the relative path
    return {"url": f"/static/uploads/{filename}", "filename": filename}
