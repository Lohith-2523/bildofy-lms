from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 10


async def validate_upload(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail="File exceeds 10MB limit",
        )

    file.file.seek(0)
