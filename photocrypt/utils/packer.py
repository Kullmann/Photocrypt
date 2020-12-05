"""
    author: Hosung Lee
    date: December 6 2020

    pack utils to combine/extract multiple meaningful data into/from one.
"""

from typing import List
from photocrypt.core import ByteStream

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
    result = []
    while stream.tell() < len(packed_data):
        result.append(stream.read(stream.read_int()))
    return result
