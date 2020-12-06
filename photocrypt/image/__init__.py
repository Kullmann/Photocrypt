"""
Image module. Provides image formats used by photocrypt.
"""

# basic image operations
from photocrypt.core.Image import Image, open_image_as, convert_image, _open_image

# import supported image formats
from .Bitmap import Bitmap
from .CryptoBitmap import CryptoBitmap

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
