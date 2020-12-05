"""
Image module. Provides image formats used by photocrypt.
"""

# basic image operations
from photocrypt.core.Image import Image, open_image_as

# import supported image formats
from .Bitmap import Bitmap
from .CryptoBitmap import CryptoBitmap
