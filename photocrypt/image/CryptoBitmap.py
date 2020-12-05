"""
    author: Hosung Lee
    date: December 5 2020

    crypto bitmap class
"""

from photocrypt.core import ImageHeader, ByteStream
from .Bitmap import *

CH_BYTES = 100
CH_LENGTH = 4 + CH_BYTES

class CryptoHeader(ImageHeader):
    """
    Class to represent bitmap file header.
    """

    protocol = [int, (bytes, [CH_BYTES])]


def create_crypto_header(*, fill_with: bytes = b'\x00'):
    """
    function to create CryptoHeader object
    :fill_with fills the header with the byte.
    """
    if len(fill_with) > 1:
        raise ValueError("fill_with value has to be 1 byte.")
    data_stream = ByteStream()
    data_stream.write_int(CH_BYTES)
    data_stream.write(fill_with * CH_BYTES)
    data_stream.seek(0)
    return CryptoHeader.read(data_stream)


class CryptoBitmap(Bitmap):
    """
    Extended Bitmap that includes a crypto header
    """
    def __init__(self, headers, data):
        super().__init__(headers, data)
        (
            self.crypto_header
        ) = headers[2]

    @classmethod
    def read(cls, data_stream: ByteStream) -> 'Bitmap':
        """
        Load bitmap from bytes
        """
        file_header, info_header = cls.read_bitmap_headers(data_stream)
        size = file_header.get_value(BF_FILE_SIZE)
        offset = file_header.get_value(BF_OFFSET)

        # using reversed_1 as indicator of cryptobitmap
        if file_header.get_value(BF_REVERSED_1) == 4362:
            crypto_header = cls.read_crypto_header(data_stream)
        else:
            # if not a cryptobitmap, convert image to cryptobitmap
            crypto_header = create_crypto_header()
            new_size = size + CH_LENGTH
            file_header.set_value(BF_FILE_SIZE, new_size)
            file_header.set_value(BF_REVERSED_1, 4362)
            new_offset = offset + CH_LENGTH
            file_header.set_value(BF_OFFSET, new_offset)

        data_stream.seek(offset)
        data = data_stream.read(info_header.get_value(BI_IMAGE_SIZE))

        new_bitmap = cls(
            [file_header, info_header, crypto_header],
            data
        )

        return new_bitmap

    @classmethod
    def read_crypto_header(cls, data_stream) -> CryptoHeader:
        """
        Reads bitmap headers from bytestream.
        """
        return CryptoHeader.read(data_stream)
