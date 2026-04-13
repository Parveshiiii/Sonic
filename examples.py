"""
Quick Start Examples for Audio Separation Library

Run with: python examples.py
"""
# written by custom llm

from src.processor import AudioProcessor
from src.audio_io import AudioIO
from src.utils import AudioUtils
import torch

def example_1_crop_audio():
    """Example 1: Crop audio from 30s to 90s"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Crop Audio")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    # Create a test audio file first
    import os
    if not os.path.exists("sample.wav"):
        print("⚠ Creating sample audio file...")
        # You would load a real audio file here
        # processor.crop("input.wav", "cropped.wav", 30, 90)
        print("  To test: processor.crop('input.wav', 'cropped.wav', 30, 90)")
    else:
        processor.crop("sample.wav", "cropped.wav", 30, 90)


def example_2_combine_audio():
    """Example 2: Combine two audio tracks"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Combine Audio Tracks")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    print("✓ Methods available: 'add', 'mean', 'subtract', 'multiply', 'divide'")
    print("✓ Command: processor.combine('track1.wav', 'track2.wav', 'output.wav', method='mean')")


def example_3_detect_bpm():
    """Example 3: Detect BPM"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Detect BPM")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    print("✓ Command: bpm = processor.detect_bpm('song.wav')")
    print("✓ Returns: BPM as float")


def example_4_speed_control():
    """Example 4: Change audio speed"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Change Audio Speed")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    print("✓ Speed up 1.5x: processor.speed_change('song.wav', 'faster.wav', 1.5)")
    print("✓ Slow down 0.5x: processor.speed_change('song.wav', 'slower.wav', 0.5)")
    print("✓ Range: 0.1 (10x slower) to 10.0 (10x faster)")


def example_5_tempo_match():
    """Example 5: Match tempo of two tracks"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Tempo Matching")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    print("✓ Both tracks will be time-stretched to their average BPM")
    print("✓ Command: processor.match_tempo('track1.wav', 'track2.wav', 'out1.wav', 'out2.wav')")


def example_6_batch_processing():
    """Example 6: Batch processing multiple operations"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Batch Processing")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    operations = [
        ("crop", ("input.wav", "cropped.wav", 0, 30)),
        ("speed_change", ("cropped.wav", "faster.wav", 1.5)),
        ("detect_bpm", ("faster.wav",)),
    ]
    
    print("✓ Processing pipeline:")
    for op_name, args in operations:
        print(f"  - {op_name}{args}")
    
    # Uncomment to run: processor.batch_process(operations)


def example_7_resample():
    """Example 7: Resample audio"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Resample Audio")
    print("="*60)
    
    processor = AudioProcessor(device="cpu")
    
    print("✓ Resample 44.1kHz to 48kHz:")
    print("  processor.resample('input.wav', 'output.wav', 48000)")


def show_available_features():
    """Display all available features"""
    print("\n" + "="*60)
    print("AVAILABLE FEATURES")
    print("="*60)
    
    features = {
        "AudioIO": [
            "load(file_path, device) - Load audio file",
            "save(audio, output_path) - Save audio file",
        ],
        "AudioCropper": [
            "crop(audio, start_time, end_time) - Trim audio",
        ],
        "AudioCombiner": [
            "combine(audio1, audio2, method) - Blend two tracks",
        ],
        "TempoShifter": [
            "shift(audio, rate) - Change speed without pitch change",
        ],
        "TempoDetector": [
            "detect_bpm(audio) - Detect BPM using onset detection",
        ],
        "TempoMatcher": [
            "match(audio1, audio2) - Sync two tracks to average BPM",
        ],
        "AudioResampler": [
            "resample(audio, target_sample_rate) - Change sample rate",
        ],
        "AudioProcessor": [
            "crop(file, output, start, end)",
            "combine(file1, file2, output, method)",
            "speed_change(file, output, rate)",
            "detect_bpm(file)",
            "match_tempo(file1, file2, out1, out2)",
            "resample(file, output, target_sr)",
            "batch_process(operations) - Execute multiple operations",
        ],
    }
    
    for module, methods in features.items():
        print(f"\n{module}:")
        for method in methods:
            print(f"  • {method}")


if __name__ == "__main__":
    print("\n╔" + "="*58 + "╗")
    print("║" + " "*10 + "Audio Separation Library - Examples" + " "*13 + "║")
    print("╚" + "="*58 + "╝")
    
    show_available_features()
    
    print("\n" + "="*60)
    print("RUNNING EXAMPLES")
    print("="*60)
    
    example_1_crop_audio()
    example_2_combine_audio()
    example_3_detect_bpm()
    example_4_speed_control()
    example_5_tempo_match()
    example_6_batch_processing()
    example_7_resample()
    
    print("\n" + "="*60)
    print("QUICK START")
    print("="*60)
    print("""
from src.processor import AudioProcessor

# Initialize
processor = AudioProcessor(device="cuda")  # or "cpu"

# Crop audio
processor.crop("song.wav", "out.wav", 30, 90)

# Combine tracks
processor.combine("vocals.wav", "backing.wav", "remix.wav", method="mean")

# Detect BPM
bpm = processor.detect_bpm("song.wav")

# Change speed
processor.speed_change("song.wav", "faster.wav", 1.5)

# Match tempos
processor.match_tempo("track1.wav", "track2.wav", "out1.wav", "out2.wav")

# Resample
processor.resample("song.wav", "output.wav", 48000)
""")
    
    print("="*60)
    print("✓ Ready to use! Check examples above.")
    print("="*60 + "\n")
