import socket
import struct
import secrets
import threading
import time
from cryptography.fernet import Fernet, InvalidToken

class DeepVirtualTCPIPStackCore:
    def __init__(self, master_key=None, target_ttl=128, window_size=65535):
        self.target_ttl = target_ttl
        self.window_size = window_size
        self._lock = threading.Lock()
        
        if master_key is None:
            self.encryption_key = Fernet.generate_key()
        else:
            self.encryption_key = master_key
            
        self.cipher = Fernet(self.encryption_key)
        self._active_sockets = {}
        self._packet_counter = 0
        self._sequence_tracker = secrets.randbelow(4294967295)

    def _generate_secure_noise(self, length: int) -> bytes:
        return secrets.token_bytes(length)

    def generate_spoofed_tcp_header(self, src_port: int, dst_port: int, seq_num: int, ack_num: int, flags: int = 0x18) -> bytes:
        with self._lock:
            self._packet_counter += 1
            data_offset_reserved = (5 << 4)
            window = self.window_size + secrets.randbelow(128) - 64
            checksum = secrets.randbits(16)
            urg_ptr = 0
            
            header = struct.pack(
                '!HHLLBBHHH',
                src_port,
                dst_port,
                seq_num,
                ack_num,
                data_offset_reserved,
                flags,
                window,
                checksum,
                urg_ptr
            )
            return header

    def inject_network_noise(self, raw_payload: bytes) -> bytes:
        with self._lock:
            noise_len = secrets.randbelow(48) + 16
            noise_chunk = self._generate_secure_noise(noise_len)
            tls_dummy_header = b'\x17\x03\x03' + struct.pack('!H', len(raw_payload) + noise_len + 12)
            timestamp_marker = struct.pack('!Q', int(time.time() * 1000000))
            obfuscated_payload = tls_dummy_header + timestamp_marker + noise_chunk + raw_payload
            return obfuscated_payload

    def strip_network_noise(self, obfuscated_payload: bytes) -> bytes:
        if len(obfuscated_payload) < 25:
            return obfuscated_payload
        try:
            stripped = obfuscated_payload[13:]
            payload_marker_idx = stripped.find(b'\x00\x01')
            if payload_marker_idx != -1 and payload_marker_idx < 64:
                return stripped[payload_marker_idx + 2:]
            return stripped[32:]
        except Exception:
            return obfuscated_payload

    def encrypt_packet_stream(self, data: bytes) -> bytes:
        noisy_data = self.inject_network_noise(data)
        encrypted_stream = self.cipher.encrypt(noisy_data)
        return encrypted_stream

    def decrypt_packet_stream(self, encrypted_data: bytes) -> bytes:
        try:
            decrypted_noisy = self.cipher.decrypt(encrypted_data)
            original_data = self.strip_network_noise(decrypted_noisy)
            return original_data
        except (InvalidToken, Exception):
            return b""

    def create_spoofed_socket(self, family=socket.AF_INET, sock_type=socket.SOCK_STREAM):
        with self._lock:
            sock_id = secrets.randbelow(55535) + 10000
            socket_params = {
                "id": sock_id,
                "ttl": self.target_ttl + secrets.choice([-2, -1, 0, 1, 2]),
                "window": self.window_size,
                "status": "VIRTUAL_ESTABLISHED",
                "created_at": time.time(),
                "sequence_base": self._sequence_tracker
            }
            self._active_sockets[sock_id] = socket_params
            return sock_id, socket_params

    def get_stack_telemetry(self) -> dict:
        with self._lock:
            return {
                "total_packets_processed": self._packet_counter,
                "active_sockets_count": len(self._active_sockets),
                "current_ttl": self.target_ttl,
                "encryption_active": True,
                "dpi_evasion_mode": "Polymorphic TLS-Mimicry + Layer 4 Tunneling"
            }

def get_virtual_tcpip_instance(master_key=None):
    return DeepVirtualTCPIPStackCore(master_key=master_key)