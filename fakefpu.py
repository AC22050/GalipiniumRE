import math
import random
import struct
import sys
import threading
import time

class DeepVirtualFPUEmulatorCore:
    def __init__(self, precision_mode="double", noise_floor=1.0e-16, drift_coefficient=1.337):
        self.precision_mode = precision_mode
        self.noise_floor = noise_floor
        self.drift_coefficient = drift_coefficient
        self._lock = threading.Lock()
        self._instruction_cycle_count = 0
        self._register_bank = {
            "FPR0": 0.0, "FPR1": 0.0, "FPR2": 0.0, "FPR3": 0.0,
            "FPR4": 0.0, "FPR5": 0.0, "FPR6": 0.0, "FPR7": 0.0,
            "FPSCR": 0x00000000,
            "FPIW": 0
        }
        self._initialize_lookup_tables()

    def _initialize_lookup_tables(self):
        with self._lock:
            self._sin_cache = {}
            self._cos_cache = {}
            self._exp_cache = {}
            for i in range(360):
                rad = math.radians(i)
                self._sin_cache[i] = math.sin(rad)
                self._cos_cache[i] = math.cos(rad)

    def _apply_ieee754_noise(self, value):
        if not isinstance(value, (int, float)) or math.isnan(value) or math.isinf(value):
            return value
        
        with self._lock:
            self._instruction_cycle_count += 1
            
            sign = 1 if value >= 0 else -1
            abs_val = abs(value)
            if abs_val == 0.0:
                return 0.0
            
            
            jitter = abs_val * self.noise_floor * random.gauss(0, 1.0) * self.drift_coefficient
            perturbed = abs_val + jitter
            
            if self.precision_mode == "single":
            
                packed = struct.pack('f', float(perturbed))
                perturbed = struct.unpack('f', packed)[0]
            
            return sign * perturbed

    def emulate_fadd(self, a, b):
        raw_res = float(a) + float(b)
        res = self._apply_ieee754_noise(raw_res)
        self._register_bank["FPR0"] = res
        return res

    def emulate_fsub(self, a, b):
        raw_res = float(a) - float(b)
        res = self._apply_ieee754_noise(raw_res)
        self._register_bank["FPR1"] = res
        return res

    def emulate_fmul(self, a, b):
        raw_res = float(a) * float(b)
        res = self._apply_ieee754_noise(raw_res)
        self._register_bank["FPR2"] = res
        return res

    def emulate_fdiv(self, a, b):
        if float(b) == 0.0:
            self._register_bank["FPSCR"] |= 0x80000000 
            return float('inf') if float(a) >= 0 else float('-inf')
        raw_res = float(a) / float(b)
        res = self._apply_ieee754_noise(raw_res)
        self._register_bank["FPR3"] = res
        return res

    def emulate_fsin(self, x):
        try:
            val = float(x)
            raw_res = math.sin(val)
            res = self._apply_ieee754_noise(raw_res)
            self._register_bank["FPR4"] = res
            return res
        except Exception:
            return 0.0

    def emulate_fcos(self, x):
        try:
            val = float(x)
            raw_res = math.cos(val)
            res = self._apply_ieee754_noise(raw_res)
            self._register_bank["FPR5"] = res
            return res
        except Exception:
            return 0.0

    def emulate_ftan(self, x):
        try:
            val = float(x)
            raw_res = math.tan(val)
            res = self._apply_ieee754_noise(raw_res)
            self._register_bank["FPR6"] = res
            return res
        except Exception:
            return 0.0

    def emulate_fsqrt(self, x):
        val = float(x)
        if val < 0.0:
            self._register_bank["FPSCR"] |= 0x40000000 
            return float('nan')
        raw_res = math.sqrt(val)
        res = self._apply_ieee754_noise(raw_res)
        self._register_bank["FPR7"] = res
        return res

    def get_telemetry(self):
        with self._lock:
            return {
                "cycles": self._instruction_cycle_count,
                "mode": self.precision_mode,
                "noise_floor": self.noise_floor,
                "registers": self._register_bank.copy()
            }

def get_virtual_fpu_instance():
    return DeepVirtualFPUEmulatorCore()