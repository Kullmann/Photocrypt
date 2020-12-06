"""
PhotoCrypt Package
"""

# basic image operations
from .image import open_image
from .image import open_image_as
from .image import convert_image

# basic byte operations
from .core.ByteData import ByteData
from .core.ByteStream import ByteStream
from .core.packer import pack
from .core.packer import unpack

# PhotoCrypt class
from .driver import Photocrypt

# encrypt and decrypt images
from .imcrypto import encrypt_image
from .imcrypto import decrypt_image
