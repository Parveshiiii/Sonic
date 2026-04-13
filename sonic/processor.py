"""Main audio processor - orchestrates all operations"""

from typing import Optional
import torch
from .types import AudioData
from .audio_io import AudioIO
from .processors import (
    AudioCropper, AudioCombiner, TempoShifter, 
    TempoDetector, TempoMatcher, AudioResampler
)
from loguru import logger

__all__ = [
    "AudioProcessor",
    "AudioIO",
    "AudioCropper",
    "AudioCombiner",
    "TempoShifter",
    "TempoDetector",
    "TempoMatcher",
    "AudioResampler",
]

class AudioProcessor:
    """
    Main audio processor - orchestrates all audio operations
    
    Example:
        processor = AudioProcessor(device="cuda")
        processor.crop("song.wav", "cropped.wav", 30, 90)
    """
    def __init__(
        self,
        device: Optional[str] = None
    ):
        """
        Initialize processor
        
        Args:
            device: "cuda" for GPU, "cpu" for CPU, None for auto-detect
        """
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        logger.success(f"✓ Audio Processor initialized on {self.device}")


    def crop(
        self,
        input_file: str,
        output_file: str,
        start: float,
        end: float
    ) -> None:
        """
        Crop audio file to time range
        
        Args:
            input_file: Input audio file path
            output_file: Output audio file path
            start: Start time in seconds
            end: End time in seconds
        """
        audio = AudioIO.load(input_file, self.device)
        cropped = AudioCropper.crop(audio, start, end)
        AudioIO.save(cropped, output_file)
        logger.success(f"✓ Cropped: {input_file} ({start}s - {end}s) → {output_file}")
    
    def combine(
        self,
        file1: str,
        file2: str,
        output_file: str,
        method: str = "mean"
    ) -> None:
        """
        Combine two audio files
        
        Args:
            file1: First audio file
            file2: Second audio file
            output_file: Output file path
            method: Blend method - "add", "mean", "subtract", "multiply", "divide"
        """
        audio1 = AudioIO.load(file1, self.device)
        audio2 = AudioIO.load(file2, self.device)
        combined = AudioCombiner.combine(audio1, audio2, method)
        AudioIO.save(combined, output_file)
        logger.success(f"✓ Combined: {file1} + {file2} ({method}) → {output_file}")

    def speed_change(
        self,
        input_file: str,
        output_file: str,
        rate: float
    ) -> None:
        """
        Change audio speed without changing pitch
        
        Args:
            input_file: Input audio file
            output_file: Output file path
            rate: Speed multiplier (2.0 = 2x faster, 0.5 = half speed)
        """
        audio = AudioIO.load(input_file, self.device)
        shifted = TempoShifter.shift(audio, rate)
        AudioIO.save(shifted, output_file)
        logger.success(f"✓ Speed changed: {input_file} (rate={rate}) → {output_file}")

    def detect_bpm(
        self,
        input_file: str
    ) -> float:
        """
        Detect BPM of audio file
        
        Args:
            input_file: Input audio file
        
        Returns:
            BPM as float
        """
        audio = AudioIO.load(input_file, self.device)
        bpm = TempoDetector.detect_bpm(audio)
        logger.success(f"✓ Detected BPM: {input_file} = {bpm:.1f}")
        return bpm

    def match_tempo(
        self,
        file1: str,
        file2: str,
        output1: str,
        output2: str
    ) -> None:
        """
        Match tempo of two files by time-stretching to average BPM
        
        Args:
            file1: First audio file
            file2: Second audio file
            output1: Output file for first track
            output2: Output file for second track
        """
        audio1 = AudioIO.load(file1, self.device)
        audio2 = AudioIO.load(file2, self.device)
        matched1, matched2 = TempoMatcher.match(audio1, audio2)
        AudioIO.save(matched1, output1)
        AudioIO.save(matched2, output2)
        logger.success(f"✓ Tempo matched: {file1} + {file2}")

    def resample(
        self,
        input_file: str,
        output_file: str,
        target_sample_rate: int
    ) -> None:
        """
        Resample audio to different sample rate
        
        Args:
            input_file: Input audio file
            output_file: Output file path
            target_sample_rate: Target sample rate in Hz (e.g., 44100, 48000)
        """
        audio = AudioIO.load(input_file, self.device)
        resampled = AudioResampler.resample(audio, target_sample_rate)
        AudioIO.save(resampled, output_file)
        logger.success(f"✓ Resampled: {input_file} → {output_file} ({target_sample_rate} Hz)")

    def batch_process(
        self,
        operations: list
    ) -> None:
        """
        Execute multiple operations in sequence
        
        Args:
            operations: List of (operation_name, args) tuples
        
        Example:
            processor.batch_process([
                ("crop", ("input.wav", "cropped.wav", 0, 30)),
                ("speed_change", ("cropped.wav", "faster.wav", 1.5)),
                ("detect_bpm", ("faster.wav",))
            ])
        """
        for op_name, args in operations:
            try:
                method = getattr(self, op_name)
                method(*args)
            except Exception as e:
                logger.error(f"✗ Error in {op_name}: {e}")



