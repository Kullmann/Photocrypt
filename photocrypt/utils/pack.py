"""
    author: Hosung Lee
    date: December 4 2020

    pack utils
"""

from typing import List
from .bytes import ByteStream

def pack(*args: bytes) -> bytes:
    """
    prepend four bytes representing number of the data to each data and merge data together.
    """
    stream = ByteStream()
    for data in args:
        stream.write_int(len(data))
        stream.write(data)
    return stream.getvalue()

def unpack(packed_data: bytes) -> List[bytes]:
    """
    parse data separated by 4 bytes header of each data. Header represents the length of the data.
    """
    stream = ByteStream(packed_data)
    while stream.tell() < len(packed_data):
        print(stream.read_int())

    return 1

p = pack(b"hello", b"world!")
print("packed: ")
print(p)
print("unpacked: ")
up = unpack(p)
