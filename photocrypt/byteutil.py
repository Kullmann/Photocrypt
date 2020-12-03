"""
    author: Hosung Lee
    date: December 4 2020

    Useful utils for bytes operation
"""
import io
import struct
a = io.BytesIO()
class ByteStream(io.BytesIO):
    """
    ByteStream class extends io.BytesIO

    added read and write method of different types.
    """
    def read_int(self,*, endian: str = 'little') -> int:
        """
        reads int from byte stream.
        """
        return int.from_bytes(self.read(4), endian)
    
    def read_short(self,*, endian: str = 'little') -> int:
        """
        reads short from byte stream.
        """
        return int.from_bytes(self.read(2), endian)

    def read_str(self, size: int = 1, encoding: str = 'utf-8') -> str:
        """
        reads string from byte stream.
        """
        return self.read(size).decode(encoding)

    def read_type(self, rtype, *args, **kwargs):
        """
        reads of type
        """
        if rtype is int:
            return self.read_int(*args, **kwargs)

        if rtype == 'short':
            return self.read_short(*args, **kwargs)

        if rtype is str:
            return self.read_str(*args, **kwargs)

        if isinstance(rtype, tuple):
            if len(rtype) == 1:
                return self.read_type(rtype[0])

            if len(rtype) == 2:
                return self.read_type(rtype[0], *rtype[1])

            if len(rtype) == 3:
                return self.read_type(rtype[0], *rtype[1], **rtype[2])

        raise TypeError(f"Cannot read this type: {rtype}")
    
    def read_complex(self, types: list) -> list:
        """
        reads as specified in the list
        example:
        bs = ByteStream(b'\x01\x00\x00\x00hello\x01\x00')
        bs.read_complex([int, (str, 5), short])
        >>> [1, "hello", 1]
        """

        return [self.read_type(t) for t in types]

    def write_int(self, data: int, *, endian: str = 'little') -> None:
        """
        writes int to byte stream.
        """
        self.write(struct.pack(('<' if endian == 'little' else '>') + 'i', data))
    
    def write_short(self, data: int, *, endian: str = 'little') -> None:
        """
        writes short to byte stream.
        """
        self.write(struct.pack(('<' if endian == 'little' else '>') + 'h', data))

    def write_str(self, data: str, encoding: str = 'utf-8') -> None:
        """
        writes string to byte stream.
        """
        return self.write(data.encode(encoding))

    def write_type(self, wtype, *args, **kwargs) -> None:
        """
        writes of type
        """
        if wtype is int:
            return self.write_int(*args, **kwargs)

        if wtype == 'short':
            return self.write_short(*args, **kwargs)

        if wtype is str:
            return self.write_str(*args, **kwargs)

        if isinstance(wtype, tuple):
            if len(wtype) == 2:
                return self.write_type(wtype[0], wtype[1])

            if len(wtype) == 3:
                return self.write_type(wtype[0], wtype[1], *wtype[2])

            if len(wtype) == 4:
                return self.write_type(wtype[0], wtype[1], *wtype[2], **wtype[3])

        raise TypeError(f"Cannot write this type: {wtype}")
    
    def write_complex(self, types: list) -> None:
        """
        write as specified in the list
        example:
        bs = ByteStream(b'\x01\x00\x00\x00hello\x01\x00')
        bs.write_complex([(int, 1), (str, "hello"), ('short', 1)])
        >>> [1, "hello", 1]
        """

        for t in types:
            self.write_type(t)

a = ByteStream(b'\x01\x15\x00\x00hello\x01\x00')
print(a.read_complex([int, (str, [5]), 'short']))
print(a.read())
b = ByteStream()

print(a.getvalue())
b.write_complex([(int, 5377), (str, "hello"), ('short', 1)])
print(b.getvalue())
