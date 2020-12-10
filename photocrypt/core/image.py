"""
    author: Hosung Lee
    date: December 7 2020

    Abstract iamge and image header classes that are base classes of
    all Images and their headers within photocrypt package.
"""

from abc import abstractmethod
from typing import Union, List
import PIL.Image
from .bstream import ByteStream
from .bdata import ByteData


class ImageHeader(ByteData):
    """
    base class to represent Image Header
    """
    protocol = []

    def __init__(self, header: list):
        self.protocol = self.__class__.protocol
        self.header = header

    @classmethod
    def get_protocol(cls) -> List[type]:
        """
        get protocol of the header

        :Return: protocol of current header.
        :rtype: List[type]
        """
        return cls.protocol

    def get_value(self, i: int) -> Union[bytes, 'short', int, str]:
        """
        get header list

            Parameters:
                i (int): index of header
            
            Returns: 
                value (any): value in ith index of header.
        """
        if i < 0 or i > len(self.header):
            raise IndexError("header index out of bounds")
        return self.header[i]

    def set_value(self, i: int, value: Union[bytes, 'short', int, str]) -> None:
        """
        sets header value

            Parameters:
                i (int): index of header
                value (any) value to set in ith index of header.
        """
        if i < 0 or i > len(self.header):
            raise IndexError("header index out of bounds")
        self.header[i] = value

    @classmethod
    def read(cls, data_stream: ByteStream) -> 'ImageHeader':
        """
        Reads ByteStream to generate a header.

            Parameters:
                data_stream (ByteStream): bytestream to read
            
            Return:
                image header (ImageHeader): image header object
        """

        return cls(data_stream.read_multiple(cls.get_protocol()))

    def write(self, data_stream: ByteStream) -> None:
        """
        Write header to a ByteStream

            Parameters:
                data_stream (ByteStream): bytestream to write
        """
        data_stream.write_multiple([
            (x[0], y) if isinstance(x, tuple) else (x, y)
            for x, y
            in zip(self.protocol, self.header)
        ])

    def __repr__(self):
        return f"<{self.__class__.__name__}>[{' | '.join(map(str,self.header))}]"


class Image(ByteData):
    """
    abstract class to represent Image types
    """
    image_format = None

    def __init__(self, headers: list, data: bytes):
        self._headers = headers
        self._data = data

    @classmethod
    @abstractmethod
    def test_format(cls, data: bytes) -> Union[str, None]:
        """
        returns name of format if data represents current format, None otherwise.

            Parameters:
                data (bytes): data that represents image.
            Returns:
                name of format (str) if data represents current format
                None otherwise.
        """
        ...

    @property
    def headers(self) -> List[ImageHeader]:
        """
        getter method of headers

            Returns:
                headers (list of image headers)
        """
        return self._headers

    @property
    def data(self) -> bytes:
        """
        getter method of data

            Returns:
                image data (bytes): data part of the image
        """
        return self._data

    @data.setter
    def data(self, data: bytes) -> None:
        """
        setter method of data

            Parameters:
                data (bytes): image data in bytes
        """
        if len(data) < len(self._data):
            raise ValueError(f"data is smaller than {len(self._data)}")

        if len(data) > len(self._data):
            self._data = data[:len(self._data)]

        else:
            self._data = data

    @classmethod
    @abstractmethod
    def read(cls, data_stream: ByteStream):
        """
        Read bytes from byte stream to construct the class.
        """
        ...

    @abstractmethod
    def write(self, data_stream: ByteStream) -> None:
        """
        write bytes to byte stream.
        """
        ...

    @classmethod
    def open(cls, file_path: str) -> 'Image':
        """
        loads image from path and converts it to specified format of class.
        """
        with open(file_path, 'rb') as file:
            head = file.read(32)
            if not cls.test_format(head):
                raise ValueError(f"File is not in a {cls.image_format}.")
            file.seek(0)
            return cls.from_bytes(file.read())

    def save(self, file_path: str) -> None:
        """
        saves image to path.
        """
        with open(file_path, 'wb') as file:
            file.write(self.to_bytes())


def open_image_as(file_path: str, as_format: Image) -> Image:
    """
    loads image from path and converts it to specified image format
    """
    try:
        return as_format.open(file_path)
    except ValueError:
        data_stream = ByteStream()
        PIL.Image.open(file_path).save(
            data_stream, format=as_format.image_format)
        data_stream.seek(0)
        return as_format.read(data_stream)


def convert_image(src: Image, to_format: Image) -> Image:
    """
    Converts an image from one type to another.
    """
    return to_format.from_bytes(src.to_bytes())


def _open_image(supported_formats: list, file_path: str) -> Image:
    """
    loads image from path to Image class.
    """
    if len(supported_formats) == 0:
        raise Exception("operation not supported yet.")
    _default_format = supported_formats[0]
    with open(file_path, 'rb') as file:
        head = file.read(32)
        for _f in supported_formats:
            if _f.test_format(head):
                return _f.open(file_path)

    return open_image_as(file_path, _default_format)
