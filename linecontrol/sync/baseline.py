"""A calibration baseline carries the generation it was taken under."""

from dataclasses import dataclass
from typing import Any, Dict

from ..ns.units import normalize_angle_deg


@dataclass(frozen=True)
class Baseline:
    baseline_id: str
    phase_deg: float
    freq_hz: float
    issued_tick: int
    expires_tick: int
    generation: int

    def is_expired(self, now: int) -> bool:
        return now > self.expires_tick

    def remaining(self, now: int) -> int:
        return max(0, self.expires_tick - now)

    def is_stale(self, generation: int) -> bool:
        return self.generation != generation

    def describe(self) -> Dict[str, Any]:
        return {
            "baseline": self.baseline_id,
            "phase_deg": self.phase_deg,
            "freq_hz": self.freq_hz,
            "issued_tick": self.issued_tick,
            "expires_tick": self.expires_tick,
            "generation": self.generation,
            "phase_normalized_deg": normalize_angle_deg(self.phase_deg),
        }

    @classmethod
    def from_record(cls, record) -> "Baseline":
        payload = record.payload
        ttl = int(payload.get("ttl_ticks", 0))
        return cls(
            baseline_id=record.record_id,
            phase_deg=float(payload["phase_deg"]),
            freq_hz=float(payload["freq_hz"]),
            issued_tick=record.tick,
            expires_tick=record.tick + ttl,
            generation=record.generation,
        )
