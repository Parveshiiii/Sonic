"""Core audio processors - combine, crop, time-shift, tempo detection"""

import math
import torch
import torchaudio.functional as F
from typing import Tuple
from .types import AudioData


class AudioCropper:
    """Crop (trim) audio to specific time range"""
    
    @staticmethod
    def crop(
        audio: AudioData,
        start_time: float,
        end_time: float,
    ) -> AudioData:
        """
        Crop audio to time range
        
        Args:
            audio: Input audio
            start_time: Start time in seconds
            end_time: End time in seconds
        
        Returns:
            Cropped audio
        
        Example:
            cropped = AudioCropper.crop(audio, start_time=30, end_time=90)
        """
        sample_rate = audio.sample_rate
        start_frame = int(start_time * sample_rate)
        end_frame = int(end_time * sample_rate)
        
        # Clamp to valid range
        max_frame = audio.waveform.shape[-1]
        start_frame = max(0, min(start_frame, max_frame - 1))
        end_frame = max(start_frame, min(end_frame, max_frame))
        
        cropped_waveform = audio.waveform[..., start_frame:end_frame]
        
        return AudioData(waveform=cropped_waveform, sample_rate=sample_rate)


class AudioCombiner:
    """Combine two audio tracks with different blend modes"""
    
    @staticmethod
    def combine(
        audio1: AudioData,
        audio2: AudioData,
        method: str = "mean",
    ) -> AudioData:
        """
        Combine two audio tracks
        
        Args:
            audio1: First audio
            audio2: Second audio
            method: Blend method - "add", "mean", "subtract", "multiply", "divide"
        
        Returns:
            Combined audio
        
        Example:
            combined = AudioCombiner.combine(vocals, backing, method="mean")
        """
        from torchaudio.transforms import Resample
        
        wf1 = audio1.waveform.squeeze(0) if audio1.waveform.ndim == 3 else audio1.waveform
        wf2 = audio2.waveform.squeeze(0) if audio2.waveform.ndim == 3 else audio2.waveform
        
        # Handle different sample rates - resample to higher
        if audio1.sample_rate != audio2.sample_rate:
            if audio1.sample_rate < audio2.sample_rate:
                resample = Resample(audio1.sample_rate, audio2.sample_rate)
                wf1 = resample(wf1)
                output_sr = audio2.sample_rate
            else:
                resample = Resample(audio2.sample_rate, audio1.sample_rate)
                wf2 = resample(wf2)
                output_sr = audio1.sample_rate
        else:
            output_sr = audio1.sample_rate
        
        # Truncate to shorter length
        min_length = min(wf1.shape[-1], wf2.shape[-1])
        wf1 = wf1[..., :min_length]
        wf2 = wf2[..., :min_length]
        
        # Apply blend method
        if method == "add":
            combined = wf1 + wf2
        elif method == "mean":
            combined = (wf1 + wf2) / 2
        elif method == "subtract":
            combined = wf1 - wf2
        elif method == "multiply":
            combined = wf1 * wf2
        elif method == "divide":
            combined = wf1 / (wf2 + 1e-8)  # Avoid division by zero
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return AudioData(waveform=combined.unsqueeze(0), sample_rate=output_sr)


class TempoShifter:
    """Change audio speed without changing pitch (phase vocoder)"""
    
    @staticmethod
    def shift(
        audio: AudioData,
        rate: float,
        fft_size: int = 2048,
    ) -> AudioData:
        """
        Time-shift audio (change speed without changing pitch)
        
        Args:
            audio: Input audio
            rate: Speed multiplier (2.0 = 2x faster, 0.5 = half speed)
            fft_size: FFT size for phase vocoder
        
        Returns:
            Time-shifted audio
        
        Example:
            faster = TempoShifter.shift(audio, rate=1.5)
            slower = TempoShifter.shift(audio, rate=0.5)
        """
        waveform = audio.waveform.squeeze(0) if audio.waveform.ndim == 3 else audio.waveform
        hop_size = fft_size // 4
        win_length = fft_size
        
        window = torch.hann_window(win_length, device=waveform.device)
        
        # STFT
        complex_spec = torch.stft(
            waveform,
            n_fft=fft_size,
            hop_length=hop_size,
            win_length=win_length,
            window=window,
            return_complex=True,
        )
        
        # Phase vocoder
        phase_advance = torch.linspace(0, math.pi * hop_size, complex_spec.shape[1])[..., None]
        stretched_spec = F.phase_vocoder(complex_spec, rate, phase_advance)
        
        # iSTFT
        shifted = torch.istft(
            stretched_spec,
            n_fft=fft_size,
            hop_length=hop_size,
            win_length=win_length,
            window=window,
        )
        
        return AudioData(waveform=shifted.unsqueeze(0), sample_rate=audio.sample_rate)


class TempoDetector:
    """Detect BPM of audio using onset detection"""
    
    @staticmethod
    def detect_bpm(audio: AudioData) -> float:
        """
        Detect BPM using librosa onset detection
        
        Args:
            audio: Input audio
        
        Returns:
            BPM as float
        
        Example:
            bpm = TempoDetector.detect_bpm(audio)
            print(f"Song is {bpm:.1f} BPM")
        """
        try:
            import librosa
            import numpy as np
        except ImportError:
            raise ImportError("librosa is required for tempo detection. Install with: pip install librosa")
        
        waveform = audio.waveform.squeeze(0) if audio.waveform.ndim == 3 else audio.waveform
        waveform_np = waveform.cpu().numpy()
        
        # Compute onset strength
        onset_env = librosa.onset.onset_strength(
            y=waveform_np,
            sr=audio.sample_rate,
            aggregate=np.median,
        )
        
        # Detect beats
        tempo, _ = librosa.beat.beat_track(
            onset_envelope=onset_env,
            sr=audio.sample_rate,
            tightness=110,
        )
        
        mean_tempo = np.mean(tempo.flatten())
        return float(max(mean_tempo, 1.0))


class TempoMatcher:
    """Match tempo of two audio tracks"""
    
    @staticmethod
    def match(audio1: AudioData, audio2: AudioData) -> Tuple[AudioData, AudioData]:
        """
        Time-stretch both tracks to their average BPM
        
        Args:
            audio1: First audio
            audio2: Second audio
        
        Returns:
            Tuple of tempo-matched audios
        
        Example:
            track1_matched, track2_matched = TempoMatcher.match(track1, track2)
        """
        bpm1 = TempoDetector.detect_bpm(audio1)
        bpm2 = TempoDetector.detect_bpm(audio2)
        avg_bpm = (bpm1 + bpm2) / 2
        
        rate1 = avg_bpm / bpm1
        rate2 = avg_bpm / bpm2
        
        matched1 = TempoShifter.shift(audio1, rate1)
        matched2 = TempoShifter.shift(audio2, rate2)
        
        return matched1, matched2


class AudioResampler:
    """Resample audio to different sample rates"""
    
    @staticmethod
    def resample(audio: AudioData, target_sample_rate: int) -> AudioData:
        """
        Resample audio to target sample rate
        
        Args:
            audio: Input audio
            target_sample_rate: Target sample rate in Hz
        
        Returns:
            Resampled audio
        
        Example:
            audio_48k = AudioResampler.resample(audio, 48000)
        """
        if audio.sample_rate == target_sample_rate:
            return audio
        
        from torchaudio.transforms import Resample
        
        waveform = audio.waveform
        resample = Resample(audio.sample_rate, target_sample_rate)
        resampled = resample(waveform)
        
        return AudioData(waveform=resampled, sample_rate=target_sample_rate)
