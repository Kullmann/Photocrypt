"""
    author: Hosung Lee
    date: December 7 2020

    Definition of Bitmap and Bitmap's header classes.
"""

from photocrypt.core import Image, ImageHeader, ByteStream

# data compression method
BI_RGB = 0
BI_RLE8 = 1
BI_RLE4 = 2
BI_BITFIELDS = 3
BI_JPEG = 4
BI_PNG = 5
BI_ALPHABITFIELDS = 6
BI_CMYK = 11
BI_CMYKRLE8 = 12
BI_CMYKRLE4 = 13

class BitmapFileHeader(ImageHeader):
    """
    class to represent bitmap file header.

    i   name            type
    =========================================
    0   signature       2 byte string
    1   file size       4 byte int
    2   reversed 1      2 byte short (unused)
    3   reversed 2      2 byte short (unused)
    4   data offset     4 byte int
    """

    protocol = [(str, [2]), int, 'short', 'short', int]

# index of bitmap file header
BF_SIGNATURE = 0
BF_FILE_SIZE = 1
BF_REVERSED_1 = 2
BF_REVERSED_2 = 3
BF_OFFSET = 4

class BitmapInfoHeader(ImageHeader):
    """
    class to represent bitmap information header.

    i   name            type
    =========================================
    0   size            4 byte int
    1   width           4 byte int
    2   height          4 byte int
    3   n_color_planes  2 byte short
    4   bpp             2 byte short
    5   compression     4 byte int
    6   image_size      4 byte int
    7   h_res           4 byte int
    8   v_res           4 byte int
    9   n_colors        4 byte int
    10  n_imp_colors    4 byte int
    """

    protocol = [*[int]*3, *['short']*2, *[int]*6]

# index of bitmap info header
BI_SIZE = 0
BI_WIDTH = 1
BI_HEIGHT = 2
BI_COLOR_PLANES = 3
BI_BPP = 4
BI_COMPRESSION = 5
BI_IMAGE_SIZE = 6
BI_HORIZ_RES = 7
BI_VERTI_RES = 8
BI_COLORS = 9
BI_IMP_COLORS = 10

class Bitmap(Image):
    """
    Image class to represent Bitmap
    """
    image_format = "BMP"

    def __init__(self, headers, data):
        super().__init__(headers, data)
        (
            self.file_header,
            self.info_header
        ) = headers[:2]

    @classmethod
    def test_format(cls, data: bytes):
        """
        returns name of format if format is valid, None otherwise.
        """
        if data.startswith(b'BM'):
            return cls.image_format
        return None

    @classmethod
    def read(cls, data_stream: ByteStream) -> 'Bitmap':
        """
        Load bitmap from bytes
        """
        file_header, info_header = cls.read_bitmap_headers(data_stream)

        data_stream.seek(file_header.get_value(BF_OFFSET))
        data = data_stream.read(info_header.get_value(BI_IMAGE_SIZE))

        new_bitmap = cls(
            [file_header, info_header],
            data
        )

        return new_bitmap

    def write(self, data_stream: ByteStream) -> None:
        """
        Get bytes of the bitmap.
        """

        for header in self.headers:
            header.write(data_stream)
        data_stream.write(self.data)

    @classmethod
    def read_bitmap_headers(cls, data_stream: ByteStream) -> (BitmapFileHeader, BitmapInfoHeader):
        """
        Reads bitmap headers from bytestream.
        """
        return BitmapFileHeader.read(data_stream), BitmapInfoHeader.read(data_stream)
