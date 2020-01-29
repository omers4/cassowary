import struct


def binary_from_stream(stream, struct_format):
    size = struct.calcsize(struct_format)
    buf = stream.read(size)
    if buf is None:
        return None
    res = struct.unpack(struct_format, buf)
    return res


def read_message_by_length(file):
    message_length_raw = file.read(4)
    message_length = struct.unpack('I', message_length_raw)[0]
    return file.read(message_length)
