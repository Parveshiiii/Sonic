from typing import Dict
from dataclasses import dataclass
from torch import Tensor

@dataclass
class AudioData:
    """Standard audio format used throughout library"""
    waveform: Tensor  # Shape: [Channels, Frames] or [Batch, Channels, Frames]
    sample_rate: int        # Hz (e.g., 44100, 48000)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary format used by processing functions"""
        return {
            "waveform": self.waveform,
            "sample_rate": self.sample_rate
        }
    @classmethod
    def from_dict(
        cls,
        data: Dict
    ):
        """Create from dictionary"""
        return cls(waveform=data["waveform"], sample_rate=data["sample_rate"])
