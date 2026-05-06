import asyncio
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.core.imagekit import get_imagekit
from app.schemas.upload import UploadOut

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_FOLDERS = {"profile", "listings", "misc"}
ALLOWED_MIMES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 8 * 1024 * 1024  # 8 MB
EXT_BY_MIME = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


@router.post("/image", response_model=UploadOut, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Form(default="misc"),
) -> UploadOut:
    if folder not in ALLOWED_FOLDERS:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"folder must be one of {sorted(ALLOWED_FOLDERS)}",
        )
    if file.content_type not in ALLOWED_MIMES:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"content_type must be one of {sorted(ALLOWED_MIMES)}",
        )

    body = await file.read()
    if len(body) == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="empty file")
    if len(body) > MAX_BYTES:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"file exceeds {MAX_BYTES // (1024 * 1024)}MB limit",
        )

    ext = EXT_BY_MIME[file.content_type]
    safe_name = f"{uuid.uuid4().hex}{ext}"
    ik = get_imagekit()

    def _do_upload():
        return ik.files.upload(
            file=body,
            file_name=safe_name,
            folder=f"/{folder}",
            use_unique_file_name=False,  # already randomized
        )

    try:
        result = await asyncio.to_thread(_do_upload)
    except Exception as exc:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY, detail=f"upload failed: {exc}"
        ) from exc

    if not result.url:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="imagekit returned no url")

    return UploadOut(
        url=result.url,
        thumbnail_url=result.thumbnail_url,
        file_id=result.file_id or "",
        name=result.name or safe_name,
        size=int(result.size) if result.size is not None else None,
        width=int(result.width) if result.width is not None else None,
        height=int(result.height) if result.height is not None else None,
    )
