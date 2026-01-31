import struct

PACKET_HELLO = 1
PACKET_DATA  = 2


def build_packet(packet_type: int, sender_name: str, payload: bytes) -> bytes:
    name_bytes = sender_name.encode("utf-8")
    return (
        bytes([packet_type]) +
        struct.pack("!H", len(name_bytes)) +
        name_bytes +
        payload
    )


def parse_packet(data: bytes):
    if len(data) < 3:
        return None

    packet_type = data[0]
    name_len = struct.unpack("!H", data[1:3])[0]
    offset = 3

    if len(data) < offset + name_len:
        return None

    sender_name = data[offset:offset + name_len].decode("utf-8")
    payload = data[offset + name_len:]

    return packet_type, sender_name, payload
