from .image.bitmap import *
from .image.base import ImageHeader
from .utils.bytes import ByteData, ByteStream
from random import randint

CH_BYTES = 100
CH_LENGTH = 4 + CH_BYTES

class CryptoHeader(ImageHeader):
    """
    class to represent bitmap file header.
    """

    protocol = [int, (bytes, [CH_BYTES])]

def create_crypto_header():
    data_stream = ByteStream()
    data_stream.write_int(CH_BYTES)
    data_stream.write(b'\x00' * CH_BYTES)
    data_stream.seek(0)
    return CryptoHeader.read(data_stream)


class CryptoBitmap(Bitmap):
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

def open_image_as_cbmp(file_path: str) -> CryptoBitmap:
    """
    loads image from path and converts it to bmp with crypto-header.
    """
    pass
        


# bitmap = open_image_as_cbmp("test.bmp")
# for h in bitmap.headers:
#     print(h)

# with open("test2.bmp", 'rb') as file:
#     CryptoBitmap.from_bytes(file.read())
from .image.base import open_image_as
cbmp = open_image_as("test2.bmp", CryptoBitmap)
print(cbmp.crypto_header)
#cbmp.save("test2.bmp")