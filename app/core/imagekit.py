from functools import lru_cache

from imagekitio import ImageKit

from app.core.config import get_settings


@lru_cache
def get_imagekit() -> ImageKit:
    s = get_settings()
    if not s.imagekit_private_key:
        raise RuntimeError("IMAGEKIT_PRIVATE_KEY is not configured")
    # SDK v5 only consumes private_key for auth. public_key + url_endpoint are
    # not needed at construction; the upload response carries the full URL.
    return ImageKit(private_key=s.imagekit_private_key)
