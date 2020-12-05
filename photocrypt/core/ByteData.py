"""
    author: Hosung Lee
    date: December 5 2020

    abstract ByteData class that can be converted from/to bytes.
"""

from abc import ABC, abstractmethod
from .ByteStream import ByteStream

class ByteData(ABC):
    """
    abstract class to represent types that use bytes.
    """
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
    def from_bytes(cls, data: bytes, offset: int = 0) -> 'ImageHeader':
        """
        Load header from bytes.
        """
        data_stream = ByteStream(data)
        data_stream.seek(offset)
        return cls.read(data_stream)

    def to_bytes(self) -> bytes:
        """
        Get bytes of header
        """
        data_stream = ByteStream()
        self.write(data_stream)
        return data_stream.getvalue()
