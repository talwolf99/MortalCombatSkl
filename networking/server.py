import socket
import threading
from typing import Tuple, Dict, Callable
from .protocol import build_packet, parse_packet, PACKET_HELLO, PACKET_DATA

class Server:
    HOST = "127.0.0.1"
    PORT = 6969
    PACKET_SIZE = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1.0)

        self.clients: Dict[Tuple[str, int], str] = {}  # addr → name
        self.handlers: Dict[int, Callable] = {}

        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None

    # ---------- Public API ----------

    def start(self):
        self.socket.bind((self.HOST, self.PORT))
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        self.socket.close()

    def on(self, packet_type: int, handler: Callable):
        """
        handler(server, sender_addr, sender_name, payload)
        """
        self.handlers[packet_type] = handler

    def send(self, addr, packet_type: int, sender_name: str, payload: bytes):
        packet = build_packet(packet_type, sender_name, payload)
        self.socket.sendto(packet, addr)

    def broadcast(self, packet_type: int, sender_name: str, payload: bytes, exclude=None):
        packet = build_packet(packet_type, sender_name, payload)
        for addr in self.clients:
            if addr != exclude:
                self.socket.sendto(packet, addr)

    # ---------- Internal ----------

    def _loop(self):
        while not self.stop_event.is_set():
            try:
                data, addr = self.socket.recvfrom(self.PACKET_SIZE)
                parsed = parse_packet(data)
                if not parsed:
                    continue

                packet_type, sender_name, payload = parsed

                # auto-register client
                if packet_type == PACKET_HELLO:
                    self.clients[addr] = sender_name
                    continue

                handler = self.handlers.get(packet_type)
                if handler:
                    handler(self, addr, sender_name, payload)

            except socket.timeout:
                continue
            except OSError:
                break