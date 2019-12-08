import struct


def binary_from_stream(stream, struct_format):
    size = struct.calcsize(struct_format)
    res = struct.unpack(struct_format, stream[0:size])
    stream = stream[size:]
    return res


def binary_from_file(f, struct_format):
    data = f.read(struct.calcsize(struct_format))
    if data is None:
        return None
    return binary_from_stream(data, struct_format)
