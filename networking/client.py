import socket
import threading
from typing import Dict, Callable
from .protocol import build_packet, parse_packet, PACKET_HELLO, PACKET_DATA

class Client:
    PACKET_SIZE = 4096

    def __init__(self, name: str):
        self.name = name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1.0)

        self.handlers: Dict[int, Callable] = {}
        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None

    # ---------- Public API ----------

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))
        self._send_hello()

        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def disconnect(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        self.socket.close()

    def on(self, packet_type: int, handler: Callable):
        """
        handler(client, sender_name, payload)
        """
        self.handlers[packet_type] = handler

    def send(self, payload: bytes):
        """
        ONLY requires payload bytes
        """
        packet = build_packet(PACKET_DATA, self.name, payload)
        self.socket.send(packet)

    # ---------- Internal ----------

    def _send_hello(self):
        packet = build_packet(PACKET_HELLO, self.name, b"")
        self.socket.send(packet)

    def _loop(self):
        while not self.stop_event.is_set():
            try:
                data = self.socket.recv(self.PACKET_SIZE)
                parsed = parse_packet(data)
                if not parsed:
                    continue

                packet_type, sender_name, payload = parsed
                handler = self.handlers.get(packet_type)
                if handler:
                    handler(self, sender_name, payload)

            except socket.timeout:
                continue
            except OSError:
                break