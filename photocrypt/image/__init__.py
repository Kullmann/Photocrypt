"""
Image module. Provides image formats used by photocrypt.
"""

# basic image operations
from photocrypt.core import Image
from photocrypt.core import open_image_as
from photocrypt.core import convert_image
from photocrypt.core.image import _open_image

# import supported image formats
from .bitmap import Bitmap
from .crypto_bitmap import CryptoBitmap

# supported formats
supported_formats = [
    CryptoBitmap,
    Bitmap
]

# open image operation
def open_image(file_path: str) -> Image:
    """
    loads image from path to Image class.
    """

    return _open_image(supported_formats, file_path)
