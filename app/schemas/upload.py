from pydantic import BaseModel


class UploadOut(BaseModel):
    url: str
    thumbnail_url: str | None = None
    file_id: str
    name: str
    size: int | None = None
    width: int | None = None
    height: int | None = None
