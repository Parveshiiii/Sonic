import torch 
from .types import AudioData
import torchaudio 
from pathlib import Path

class AudioIO:
    """Load and save audio files"""
    @staticmethod
    def load(
        file_path: str,
        device: torch.device = None
    ) -> AudioData:
        """
        Load audio file into AudioData format
        
        Args:
            file_path: Path to audio file (MP3, WAV, FLAC, etc.)
            device: torch.device to load onto (default: CPU)
        
        Returns:
            AudioData with waveform and sample_rate
        
        Example:
            audio = AudioIO.load("song.mp3")
            print(f"Duration: {audio.waveform.shape[-1] / audio.sample_rate}s")
        """
        if device is None:
            device = torch.device("cpu")
        
        waveform, sample_rate = torchaudio.load(file_path)
        waveform = waveform.to(device)
        
        # Add batch dimension if needed
        if waveform.ndim == 2:
            waveform = waveform.unsqueeze(0)
        
        return AudioData(waveform=waveform, sample_rate=sample_rate)
    @staticmethod
    def save(
        audio: AudioData,
        output_path: str
    ) -> None:
        """
        Save audio to file
        
        Args:
            audio: AudioData to save
            output_path: Output file path
        
        Example:
            AudioIO.save(audio, "output.wav")
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Remove batch dimension if present
        waveform = audio.waveform
        if waveform.ndim == 3:
            waveform = waveform.squeeze(0)
        
        torchaudio.save(output_path, waveform.cpu(), audio.sample_rate)

        print(f"✓ Audio successfully saved at {output_path}")
