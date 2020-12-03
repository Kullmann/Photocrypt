"""
    author: Hosung Lee
    date: December 4 2020

    Useful classes for managing iamges
"""
from abc import ABC, abstractmethod
from typing import Callable

class ByteData(ABC):
    """
    abstract class to represent types that use bytes.
    """
    @staticmethod
    @abstractmethod
    def from_bytes(data: bytes, offset: int = 0):
        """
        Load bitmap header from bytes.
        """
        ...

    @abstractmethod
    def to_bytes(self) -> bytes:
        """
        Get bytes of the header
        """
        ...

class Image(ByteData):
    """
    abstract class to represent Image types
    """
    def __init__(self, data: bytes):
        self._data = data

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
        if len(data) < len(self._data):
            raise Exception(f"data has to be >= {len(self.data)}")

        if len(data) > len(self._data):
            self._data = data[:len(self._data)]

        else:
            self._data = data

    def apply(self, func: Callable[[bytes], bytes]) -> None:
        """
        applies function to the data bytes of image.
        """
        self.data = func(self.data)

    @staticmethod
    @abstractmethod
    def open(file_path: str) -> 'Image':
        """
        loads image from path.
        """
        ...

    @abstractmethod
    def save(self, file_path: str) -> None:
        """
        saves image to path.
        """
        ...
