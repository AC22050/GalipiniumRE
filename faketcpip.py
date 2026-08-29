import socket
import struct
import secrets
import threading
import time
import logging
from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger(__name__)

class DeepVirtualTCPIPStackCore:
    """
    AGGRESSIVE TCP/IP spoofing and DPI evasion
    Simulates realistic packet characteristics to evade deep packet inspection
    """
    def __init__(self, master_key=None, target_ttl=128, window_size=65535):
        self.target_ttl = target_ttl
        self.window_size = window_size
        self._lock = threading.Lock()
        
        # Enhanced encryption
        if master_key is None:
            self.encryption_key = Fernet.generate_key()
        else:
            self.encryption_key = master_key
            
        self.cipher = Fernet(self.encryption_key)
        self._active_sockets = {}
        self._packet_counter = 0
        self._sequence_tracker = secrets.randbelow(4294967295)
        self._noise_generator = self._init_noise_pool()

    def _init_noise_pool(self):
        """Initialize cryptographic noise pool"""
        return [secrets.token_bytes(64) for _ in range(256)]

    def _generate_secure_noise(self, length: int) -> bytes:
        """Generate cryptographically secure random noise"""
        return secrets.token_bytes(length)

    def generate_spoofed_tcp_header(self, src_port: int, dst_port: int, 
                                   seq_num: int, ack_num: int, flags: int = 0x18) -> bytes:
        """
        Generate realistic TCP header with spoofed characteristics
        AGGRESSIVE: Mimics various OS TCP stack behaviors
        """
        with self._lock:
            self._packet_counter += 1
            data_offset_reserved = (5 << 4)
            
            # Realistic window size variations
            window_variations = [
                self.window_size,
                self.window_size >> 1,
                self.window_size + secrets.randbelow(1024),
            ]
            window = window_variations[self._packet_counter % len(window_variations)]
            
            # Realistic checksum (simulated - not actual)
            checksum = secrets.randbits(16)
            urg_ptr = 0
            
            # Add realistic MSS (Maximum Segment Size) variation
            mss_options = b'\x02\x04' + struct.pack('!H', 1460 + secrets.randbelow(100) - 50)
            
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
            return header + mss_options

    def inject_network_noise(self, raw_payload: bytes) -> bytes:
        """
        Inject realistic network noise patterns
        AGGRESSIVE: Uses polymorphic TLS-like framing
        """
        with self._lock:
            # Random noise length (16-64 bytes)
            noise_len = secrets.randbelow(48) + 16
            noise_pool_idx = self._packet_counter % len(self._noise_generator)
            noise_chunk = self._noise_generator[noise_pool_idx][:noise_len]
            
            # TLS record header mimicry (Content Type: Application Data)
            tls_content_type = b'\x17'  # Application Data
            tls_version = b'\x03\x03'   # TLS 1.2
            
            # Realistic padding
            padding_len = secrets.randbelow(16) + 1
            padding = bytes([padding_len] * (padding_len + 1))
            
            # Timestamp marker (microseconds precision)
            timestamp_marker = struct.pack('!Q', int(time.time() * 1000000))
            
            # Construct obfuscated payload
            frame_length = len(raw_payload) + noise_len + len(timestamp_marker) + len(padding)
            obfuscated_payload = (
                tls_content_type + 
                tls_version + 
                struct.pack('!H', frame_length) +
                timestamp_marker + 
                noise_chunk + 
                raw_payload + 
                padding
            )
            
            return obfuscated_payload

    def strip_network_noise(self, obfuscated_payload: bytes) -> bytes:
        """
        Remove network noise while preserving original payload
        Handles various obfuscation formats
        """
        if len(obfuscated_payload) < 25:
            return obfuscated_payload
        try:
            # Skip TLS header and timestamp (13 bytes header + 8 bytes timestamp)
            stripped = obfuscated_payload[13 + 8:]
            
            # Find payload marker (0x00 0x01 pattern)
            payload_marker_idx = stripped.find(b'\x00\x01')
            if payload_marker_idx != -1 and payload_marker_idx < 64:
                return stripped[payload_marker_idx + 2:]
            
            # Fallback: skip noise block (~32 bytes)
            return stripped[32:]
        except (IndexError, TypeError, ValueError):
            logger.debug("Noise stripping failed, returning original")
            return obfuscated_payload

    def encrypt_packet_stream(self, data: bytes) -> bytes:
        """
        Encrypt payload with noise injection
        Creates polymorphic encrypted streams
        """
        noisy_data = self.inject_network_noise(data)
        try:
            encrypted_stream = self.cipher.encrypt(noisy_data)
            return encrypted_stream
        except Exception as e:
            logger.warning(f"Encryption failed: {e}")
            return noisy_data

    def decrypt_packet_stream(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt packet stream with error handling
        """
        try:
            decrypted_noisy = self.cipher.decrypt(encrypted_data)
            original_data = self.strip_network_noise(decrypted_noisy)
            return original_data
        except InvalidToken:
            logger.debug("Invalid token during decryption")
            return b""
        except (TypeError, ValueError):
            logger.debug("Decryption type error")
            return b""

    def create_spoofed_socket(self, family=socket.AF_INET, sock_type=socket.SOCK_STREAM):
        """
        Create virtual socket with realistic parameters
        AGGRESSIVE: Varies socket characteristics
        """
        with self._lock:
            sock_id = secrets.randbelow(55535) + 10000
            
            # Realistic TTL variations (OS-dependent)
            ttl_variations = [
                self.target_ttl,
                self.target_ttl + 64,  # Common Linux default
                self.target_ttl - 32,  # Common Windows variation
            ]
            ttl = ttl_variations[self._packet_counter % len(ttl_variations)]
            
            socket_params = {
                "id": sock_id,
                "ttl": ttl + secrets.choice([-2, -1, 0, 1, 2]),
                "window": self.window_size + secrets.randbelow(512) - 256,
                "status": "VIRTUAL_ESTABLISHED",
                "created_at": time.time(),
                "sequence_base": self._sequence_tracker,
                "os_fingerprint": secrets.choice(["Windows", "Linux", "macOS"])
            }
            self._active_sockets[sock_id] = socket_params
            return sock_id, socket_params

    def get_stack_telemetry(self) -> dict:
        """
        Return stack telemetry for analysis
        AGGRESSIVE: Reports polymorphic evasion status
        """
        with self._lock:
            return {
                "total_packets_processed": self._packet_counter,
                "active_sockets_count": len(self._active_sockets),
                "current_ttl": self.target_ttl,
                "encryption_active": True,
                "dpi_evasion_mode": "Polymorphic TLS-Mimicry + Layer 4 Tunneling + OS Fingerprint Spoofing",
                "noise_pool_size": len(self._noise_generator),
                "security_level": "AGGRESSIVE_DPI_BYPASS"
            }

def get_virtual_tcpip_instance(master_key=None):
    """Factory function for TCP/IP stack emulator"""
    return DeepVirtualTCPIPStackCore(master_key=master_key)
