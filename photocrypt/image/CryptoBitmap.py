"""
    author: Hosung Lee
    date: December 5 2020

    crypto bitmap class
"""

from photocrypt.core import ImageHeader, ByteStream, packer
from .Bitmap import Bitmap, BitmapFileHeader, BF_FILE_SIZE, BF_OFFSET, BF_REVERSED_1, BI_IMAGE_SIZE

class CryptoHeader(ImageHeader):
    """
    Class to represent bitmap file header.

    i   name        type
    0   length      int (4 bytes)
    1   data        n bytes
    """

    protocol = [int, (bytes, [0])]

    def set_length(self, length: int):
        """
        Set length of data
        """
        self.protocol = [int, (bytes, [length])]

    def get_length(self):
        """
        get length of data in protocol
        """
        return self.protocol[1][1][0]


def create_crypto_header():
    """
    function to create CryptoHeader object
    """
    return CryptoHeader([0, b''])


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
    def test_format(cls, data: bytes):
        """
        returns name of format if format is valid, None otherwise.
        """
        if data.startswith(b'BM') and data[6:8] == b'\n\x11':
            return cls.image_format
        return None

    def store_crypto_information(self, *data: bytes):
        """
        Store
        """
        data = packer.pack(*data)
        self.crypto_header.set_value(1, data)
        self.crypto_header.set_value(0, len(data))
        self.crypto_header.set_length(len(data))

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
            print("test")
            print(file_header)
            crypto_header = cls.read_crypto_header(data_stream)
            file_header.set_value(BF_FILE_SIZE, size - crypto_header.get_length() - 4)
            file_header.set_value(BF_OFFSET, offset - crypto_header.get_length() - 4)
            print(file_header)

        else:
            # if not a cryptobitmap, convert image to cryptobitmap
            crypto_header = create_crypto_header()
            file_header.set_value(BF_REVERSED_1, 4362)
            offset += crypto_header.get_length()

        data_stream.seek(offset)
        data = data_stream.read(info_header.get_value(BI_IMAGE_SIZE))

        new_bitmap = cls(
            [file_header, info_header, crypto_header],
            data
        )

        return new_bitmap

    def write(self, data_stream: ByteStream) -> None:
        """
        Get bytes of the bitmap.
        """
        size = self.file_header.get_value(BF_FILE_SIZE)
        offset = self.file_header.get_value(BF_OFFSET)
        cdata_length = self.crypto_header.get_length()
        new_size, new_offset = size + cdata_length + 4, offset + cdata_length + 4

        self.headers[0] = self.file_header = BitmapFileHeader(
            [self.file_header.header[0]] +
            [new_size] +
            self.file_header.header[2:4] +
            [new_offset]
        )
        super().write(data_stream)
        self.headers[0] = self.file_header = BitmapFileHeader(
            [self.file_header.header[0]] +
            [size] +
            self.file_header.header[2:4] +
            [offset]
        )

    @classmethod
    def read_crypto_header(cls, data_stream) -> CryptoHeader:
        """
        Reads bitmap headers from bytestream.
        """
        size = data_stream.read_int()
        print(size)
        data = data_stream.read(size)
        new_header = CryptoHeader([size, data])
        new_header.set_length(size)
        return new_header
