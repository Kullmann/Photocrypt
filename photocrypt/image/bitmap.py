"""
    author: Hosung Lee
    date: December 4 2020

    Definition of Bitmap and Bitmap's header classes.
"""
import io
from struct import pack
import PIL.Image
from .imutil import ByteData, Image
from photocrypt.byteutil import ByteStream

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

class BitmapFileHeader(ByteData):
    """
    class to represent bitmap file header.
    """
    def __init__(
        self, signature: str,
        file_size: int,
        reversed_1: bytes,
        reversed_2: bytes,
        data_offset: int
        ):

        self.signature = signature
        self.file_size = file_size
        # unused
        self.reversed_1 = reversed_1
        # unused
        self.reversed_2 = reversed_2
        self.data_offset = data_offset

    @staticmethod
    def from_bytes(data: bytes, offset: int = 0) -> 'BitmapFileHeader':
        """
        Load bitmap file header from bytes.
        """
        data_stream = ByteStream(data)
        data_stream.seek(offset)

        new_header = BitmapFileHeader(
            data_stream.read(2).decode('ascii'),
            int.from_bytes(data_stream.read(4), 'little'),
            data_stream.read(2),
            data_stream.read(2),
            int.from_bytes(data_stream.read(4), 'little')
        )

        return new_header

    def to_bytes(self) -> bytes:
        """
        Get bytes of bitmap file header
        """
        data_stream = ByteStream()
        data_stream.write(self.signature.encode('ascii'))
        data_stream.write(pack('<I', self.file_size))
        data_stream.write(self.reversed_1)
        data_stream.write(self.reversed_2)
        data_stream.write(pack('<I', self.data_offset))

        return data_stream.getvalue()


class BitmapInfoHeader(ByteData):
    """
    class to represent bitmap information header.
    """
    def __init__(
        self,
        size: int,
        width: int,
        height: int,
        n_color_planes: int,
        bpp: int,
        compression: int,
        image_size: int,
        h_res: int,
        v_res: int,
        n_colors: int,
        n_imp_colors: int,
        ):

        self.size = size
        self.width = width
        self.height = height
        self.n_color_planes = n_color_planes
        self.bpp = bpp
        self.compression = compression
        self.image_size = image_size
        self.h_res = h_res
        self.v_res = v_res
        self.n_colors = n_colors
        self.n_imp_colors = n_imp_colors

    @staticmethod
    def from_bytes(data: bytes, offset: int = 0) -> 'BitmapInfoHeader':
        """
        Load bitmap information header from bytes.
        """
        data_stream = ByteStream(data)
        data_stream.seek(offset)

        new_header = BitmapInfoHeader(
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(2), 'little'),
            int.from_bytes(data_stream.read(2), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
            int.from_bytes(data_stream.read(4), 'little'),
        )

        return new_header

    def to_bytes(self):
        """
        Get bytes of the bitmap information header.
        """
        data_stream = ByteStream()
        data_stream.write(pack('<I', self.size))
        data_stream.write(pack('<I', self.width))
        data_stream.write(pack('<I', self.height))
        data_stream.write(pack('<H', self.n_color_planes))
        data_stream.write(pack('<H', self.bpp))
        data_stream.write(pack('<I', self.compression))
        data_stream.write(pack('<I', self.image_size))
        data_stream.write(pack('<I', self.h_res))
        data_stream.write(pack('<I', self.v_res))
        data_stream.write(pack('<I', self.n_colors))
        data_stream.write(pack('<I', self.n_imp_colors))
        return data_stream.getvalue()


class Bitmap(Image):
    """
        Load bitmap information header from bytes.
        """
    def __init__(self, file_header: BitmapFileHeader, info_header: BitmapInfoHeader, data: bytes):
        super().__init__(data)
        self.file_header = file_header
        self.info_header = info_header

    @staticmethod
    def from_bytes(data: bytes, offset: int = 0) -> 'Bitmap':
        """
        Load bitmap from bytes
        """
        file_header = BitmapFileHeader.from_bytes(data)
        info_header = BitmapInfoHeader.from_bytes(data, 14)

        data_stream = ByteStream(data)
        data_stream.seek(file_header.data_offset)
        data = data_stream.read(info_header.image_size)

        new_bitmap = Bitmap(
            file_header,
            info_header,
            data
        )
        
        return new_bitmap

    def to_bytes(self) -> bytes:
        """
        Get bytes of the bitmap.
        """
        return self.file_header.to_bytes() + self.info_header.to_bytes() + self._data
    
    @staticmethod
    def open(file_path: str) -> 'Bitmap':
        """
        open an image and converts it to Bitmap.
        """
        image = PIL.Image.open(file_path)
        byte_arr = ByteStream()
        image.save(byte_arr, format='BMP')
        return Bitmap.from_bytes(byte_arr.getvalue())
    
    def save(self, file_path: str) -> None:
        """
        saves current image to file path.
        """
        image = PIL.Image.open(ByteStream(self.to_bytes()))
        image.save(file_path)
