import torch 
from .types import AudioData

class AudioUtils:
    """Helper functions for audio processing"""
    @staticmethod
    def ensure_stereo(
        waveform: torch.Tensor
    ) -> torch.Tensor:
        """
        Convert any channel configuration to stereo
        
        Handles:
        - Mono [1, frames] → Stereo [2, frames] (duplicate channel)
        - Multi-channel [n, frames] → Stereo [2, frames] (downmix to stereo)
        - Batched formats [batch, channels, frames]
        
        Args:
            waveform: Audio tensor
        
        Returns:
            Stereo tensor [2, frames] or [batch, 2, frames]
        """
        if waveform.ndim not in (2, 3):
            raise ValueError(f"Expected 2D or 3D tensor, got {waveform.ndim}D")
        
        is_batched = waveform.ndim == 3
        channels_dim = 1 if is_batched else 0
        
        # Already stereo
        if waveform.shape[channels_dim] == 2:
            return waveform
        
        # Mono - duplicate channel
        elif waveform.shape[channels_dim] == 1:
            return waveform.repeat(1, 2, 1) if is_batched else waveform.repeat(2, 1)
        
        # Multi-channel - downmix to stereo
        else:
            return waveform.narrow(channels_dim, 0, 2)
    
    @staticmethod
    def get_duration(
        audio: AudioData
    ) -> float:
        """Get audio duration in seconds"""
        return audio.waveform.shape[-1] / audio.sample_rate
    @staticmethod
    def normalize(
        waveform: torch.Tensor,
        target_db: float = -20.0
    ) -> torch.Tensor:
        """
        Normalize audio to target loudness
        
        Args:
            waveform: Audio tensor
            target_db: Target loudness in dB
        
        Returns:
            Normalized waveform
        """
        # Calculate RMS
        rms = torch.sqrt(torch.mean(waveform ** 2))
        
        if rms == 0:
            return waveform
        
        # Convert dB to linear
        target_linear = 10 ** (target_db / 20.0)
        
        # Scale
        return waveform * (target_linear / rms)
