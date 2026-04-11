"""Audio Processing Library - Pure Python Audio Processing

A complete audio processing library with no external UI requirements.
Supports separation, combination, tempo detection, time-shifting, and resampling.

Example:
    from src.processor import AudioProcessor
    
    processor = AudioProcessor(device="cuda")
    processor.crop("song.wav", "cropped.wav", 30, 90)
    bpm = processor.detect_bpm("song.wav")
    processor.combine("vocals.wav", "backing.wav", "remix.wav", method="mean")
"""

from .types import AudioData
from .audio_io import AudioIO
from .utils import AudioUtils
from .processors import (
    AudioCropper,
    AudioCombiner,
    TempoShifter,
    TempoDetector,
    TempoMatcher,
    AudioResampler,
)
from .processor import AudioProcessor

__version__ = "0.1.0"
__all__ = [
    "AudioData",
    "AudioIO",
    "AudioUtils",
    "AudioCropper",
    "AudioCombiner",
    "TempoShifter",
    "TempoDetector",
    "TempoMatcher",
    "AudioResampler",
    "AudioProcessor",
]
