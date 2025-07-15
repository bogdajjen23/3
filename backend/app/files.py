import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/uploads")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    uid = f"{uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, uid)
    try:
        with open(path, "wb") as f:
            f.write(await file.read())
    except Exception:
        raise HTTPException(500, "Cannot save file")
    return {"filename": file.filename, "url": f"/files/{uid}"}
