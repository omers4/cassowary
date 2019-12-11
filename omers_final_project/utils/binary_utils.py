import struct


def binary_from_stream(stream, struct_format):
    size = struct.calcsize(struct_format)
    buf = stream.read(size)
    if buf is None:
        return None
    res = struct.unpack(struct_format, buf)
    return res


def binary_from_file(f, struct_format):
    return binary_from_stream(f, struct_format)
