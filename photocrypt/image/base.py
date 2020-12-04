"""
    author: Hosung Lee
    date: December 4 2020

    base classes for iamge and image header
"""

from typing import Callable
from abc import abstractmethod
from photocrypt.utils.bytes import ByteStream, ByteData
import PIL.Image

class ImageHeader(ByteData):
    """
    abstract class to represent Image Header
    """
    protocol = []
    def __init__(self, protocol: list, header: list):
        self.protocol = protocol
        self.header = header

    @classmethod
    def get_protocol(cls) -> list:
        """
        get protocol of the header
        """
        return cls.protocol

    def get_value(self, i: int):
        """
        get header list

        :i index of header
        """
        if i < 0 or i > len(self.header):
            raise IndexError("header index out of bounds")
        return self.header[i]

    def set_value(self, i:int, value) -> None:
        """
        sets header value

        :i index of header
        :value value to set
        """
        if i < 0 or i > len(self.header):
            raise IndexError("header index out of bounds")
        self.header[i] = value

    @classmethod
    def read(cls, data_stream: ByteStream) -> 'ImageHeader':
        """
        Reads ByteStream to generate a header.
        """

        return cls(cls.get_protocol(), data_stream.read_multiple(cls.get_protocol()))

    def write(self, data_stream: ByteStream) -> None:
        """
        Write header to a ByteStream
        """
        data_stream.write_multiple([
            (x[0], y) if isinstance(x, tuple) else (x, y)
            for x, y
            in zip(self.protocol, self.header)
        ])
    
    def __repr__(self):
        return "|".join(map(str,self.header))


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
    def test_format(cls, data: bytes):
        """
        returns name of format if format is valid, None otherwise.
        """
        ...

    @property
    def headers(self) -> list:
        """
        getter method of headers
        """
        return self._headers

    @property
    def data(self) -> bytes:
        """
        getter method of data
        """
        return self._data

    @data.setter
    def data(self, data: bytes) -> None:
        """
        setter method of data
        """
        if len(data) > len(self._data):
            self._data = data[:len(self._data)]

        else:
            self._data = data

    def apply(self, func: Callable[[bytes], bytes]) -> None:
        """
        applies function to the data bytes of image.
        """
        self.data = func(self.data)

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
        PIL.Image.open(file_path).save(data_stream, format=as_format.image_format)
        data_stream.seek(0)
        return as_format.read(data_stream)
