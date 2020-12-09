"""
    author: Hosung Lee
    date: December 7 2020

    packer combines/extracts multiple meaningful data into/from one.
    When packer packs, it prepends size of each data (4 byte integer) to separate the data.
    b'<length1><data1><length2><data2>...<length_n><data_n>'
"""

from typing import List
from .bstream import ByteStream

def pack(*args: bytes) -> bytes:
    """
    prepend four bytes representing number of the data to each data and merge data together.

    >>> pack(b'\x00\x01', b'\x11\x12\x13', b'\xf1')
    
    b'\x02\x00\x00\x00\x00\x01\x03\x00\x00\x00\x11\x12\x13\x01\x00\x00\x00\xf1'
    """
    stream = ByteStream()
    for data in args:
        stream.write_int(len(data))
        stream.write(data)
    return stream.getvalue()

def unpack(packed_data: bytes) -> List[bytes]:
    """
    parse data separated by 4 bytes header of each data. Header represents the length of the data.

    >>> unpack(b'\x02\x00\x00\x00\x00\x01\x03\x00\x00\x00\x11\x12\x13\x01\x00\x00\x00\xf1')


    """
    stream = ByteStream(packed_data)
    result = []
    while stream.tell() < len(packed_data):
        result.append(stream.read(stream.read_int()))
    return result

if __name__ == '__main__':
    print(pack(b'\x00\x01', b'\x11\x12\x13', b'\xf1'))
    print(unpack(b'\x02\x00\x00\x00\x00\x01\x03\x00\x00\x00\x11\x12\x13\x01\x00\x00\x00\xf1'))
