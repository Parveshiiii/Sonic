# Audio Separation Library 🎵

**Pure Python audio processing library** - No external UI required. Crop, combine, match tempos, detect BPM, and shift audio.

> Note: comments and explanations were written by AI for better clarity 

## Features

✅ **Audio Cropping** - Trim audio to specific time ranges  
✅ **Audio Combining** - Blend two tracks (add, mean, subtract, multiply, divide)  
✅ **BPM Detection** - Detect tempo using onset detection  
✅ **Tempo Matching** - Time-stretch tracks to same BPM  
✅ **Speed Control** - Change speed without pitch changes (phase vocoder)  
✅ **Resampling** - Convert between sample rates  
✅ **GPU Acceleration** - CUDA support for faster processing  
✅ **Batch Processing** - Execute multiple operations sequentially  

## Installation

### Using `uv` (recommended)

```bash
uv pip install -e .
```

### Using `pip`

```bash
pip install -e .
```

## Quick Start

```python
from sonic.processor import AudioProcessor

# Initialize processor
processor = AudioProcessor(device="cuda")  # or "cpu" for CPU

# Crop audio from 30s to 90s
processor.crop("input.wav", "cropped.wav", 30, 90)

# Combine two tracks
processor.combine("vocals.wav", "backing.wav", "remix.wav", method="mean")

# Detect BPM
bpm = processor.detect_bpm("song.wav")
print(f"BPM: {bpm:.1f}")

# Change speed (1.5x faster)
processor.speed_change("song.wav", "faster.wav", 1.5)

# Match tempo of two tracks
processor.match_tempo("track1.wav", "track2.wav", "out1.wav", "out2.wav")

# Resample to 48kHz
processor.resample("song.wav", "output.wav", 48000)
```

## API Reference

### AudioProcessor

Main orchestrator class for all audio operations.

```python
processor = AudioProcessor(device="cuda")  # or "cpu", or None for auto
```

#### Methods

| Method | Description |
|--------|-------------|
| `crop(input, output, start, end)` | Crop audio to time range (seconds) |
| `combine(file1, file2, output, method)` | Combine two audio tracks |
| `speed_change(input, output, rate)` | Change speed (2.0 = 2x faster, 0.5 = half speed) |
| `detect_bpm(input)` | Detect BPM, returns float |
| `match_tempo(file1, file2, out1, out2)` | Time-stretch both to average BPM |
| `resample(input, output, target_sr)` | Resample to target sample rate |
| `batch_process(operations)` | Execute multiple operations sequentially |

### AudioIO

Load and save audio files.

```python
from sonic.audio_io import AudioIO
from sonic.types import AudioData

# Load audio
audio = AudioIO.load("song.wav", device="cpu")

# Save audio
AudioIO.save(audio, "output.wav")
```

### Individual Processors

Use individual processors for more control:

```python
from sonic.processors import (
    AudioCropper, AudioCombiner, TempoShifter,
    TempoDetector, TempoMatcher, AudioResampler
)

# Crop
audio = AudioIO.load("song.wav")
cropped = AudioCropper.crop(audio, start_time=30, end_time=90)

# Combine
audio1 = AudioIO.load("track1.wav")
audio2 = AudioIO.load("track2.wav")
combined = AudioCombiner.combine(audio1, audio2, method="mean")

# Tempo shift
shifted = TempoShifter.shift(audio, rate=1.5)

# Detect BPM(Beats per minute)
bpm = TempoDetector.detect_bpm(audio)

# Match tempo
matched1, matched2 = TempoMatcher.match(audio1, audio2)

# Resample
resampled = AudioResampler.resample(audio, target_sample_rate=48000)
```

### AudioUtils

Helper functions for audio manipulation.

```python
from sonic.utils import AudioUtils
from sonic.types import AudioData

# Ensure stereo
stereo_waveform = AudioUtils.ensure_stereo(waveform)

# Get duration
duration = AudioUtils.get_duration(audio)  # seconds

# Normalize
normalized = AudioUtils.normalize(waveform, target_db=-20.0)
```

## Data Types

All audio is represented as `AudioData`:

```python
from sonic.types import AudioData

audio = AudioData(
    waveform=torch.tensor(...),  # Shape: [Channels, Frames]
    sample_rate=44100             # Hz
)

# Convert to dict
audio_dict = audio.to_dict()

# Convert from dict
audio = AudioData.from_dict({"waveform": wf, "sample_rate": 44100})
```

### Waveform Shapes

- **Mono**: `[1, frames]`
- **Stereo**: `[2, frames]`
- **Multi-channel**: `[n, frames]`
- **Batched**: `[batch, channels, frames]`

## Blend Methods (Combine)

When combining two tracks, you can use different blend modes:

| Method | Formula | Use Case |
|--------|---------|----------|
| `"add"` | `w1 + w2` | Mix tracks loudly |
| `"mean"` | `(w1 + w2) / 2` | Standard mix (preserve amplitude) |
| `"subtract"` | `w1 - w2` | Difference/karaoke effect |
| `"multiply"` | `w1 * w2` | Volume modulation |
| `"divide"` | `w1 / w2` | Dynamic range compression |

```python
processor.combine("track1.wav", "track2.wav", "output.wav", method="mean")
```

## Speed Rates

For time-shifting/tempo change:

| Rate | Effect |
|------|--------|
| 2.0 | 2x speed (half duration) |
| 1.5 | 1.5x speed |
| 1.0 | No change |
| 0.5 | Half speed (double duration) |
| 0.1 | 10x slower |

Supported range: **0.1 to 10.0**

```python
processor.speed_change("song.wav", "output.wav", rate=1.5)
```

## Batch Processing

Execute multiple operations sequentially:

```python
operations = [
    ("crop", ("input.wav", "cropped.wav", 0, 30)),
    ("speed_change", ("cropped.wav", "faster.wav", 1.5)),
    ("detect_bpm", ("faster.wav",)),
]

processor.batch_process(operations)
```

## GPU Acceleration

Use CUDA for 5-10x speedup on large files:

```python
processor = AudioProcessor(device="cuda")  # GPU
# or
processor = AudioProcessor(device="cpu")   # CPU (slower)
# or
processor = AudioProcessor()               # Auto-detect
```

## Examples

### Example 1: Extract Chorus

```python
from sonic.processor import AudioProcessor

processor = AudioProcessor()

# Extract chorus section (45s to 2:15)
processor.crop("song.wav", "chorus.wav", start=45, end=135)
```

### Example 2: Create Remix

```python
# Separate vocals and backing track, then remix
processor.combine("vocals.wav", "new_backing.wav", "remix.wav", method="mean")
```

### Example 3: Sync Two Tracks

```python
# Make two songs play at same tempo
processor.match_tempo("song1.wav", "song2.wav", "song1_matched.wav", "song2_matched.wav")
```

### Example 4: Check BPM

```python
bpm = processor.detect_bpm("song.wav")
print(f"This song is {bpm:.0f} BPM")
```

### Example 5: Speed Up Music Video

```python
# Make video background music 1.2x faster
processor.speed_change("bgm.wav", "bgm_faster.wav", rate=1.2)
```

## Troubleshooting

### "CUDA out of memory"
- Use `device="cpu"` instead
- Process larger files in chunks

### "librosa not found"
- Install: `pip install librosa`
- Required for BPM detection and tempo matching

### "Unsupported audio format"
- Supported: WAV, MP3, FLAC, OGG, etc. (via `torchaudio`)
- Ensure `ffmpeg` is installed for MP3 support

### "No GPU found"
- Automatically falls back to CPU
- Or explicitly use `device="cpu"`

## Dependencies

- **torch** >= 2.0.0 - Tensor operations
- **torchaudio** >= 2.0.0 - Audio I/O and processing
- **librosa** >= 0.10.0 - BPM detection
- **numpy** >= 1.20.0 - Numerical operations

## Performance Tips

1. **Use GPU** for large files (5-10x speedup)
2. **Batch processing** to avoid repeated loading
3. **Reduce chunk size** for files with less VRAM
4. **Pre-normalize** audio for consistent results

## Project Structure

```
audio-seperation/
├── sonic/
│   ├── __init__.py           # Package exports
│   ├── types.py              # AudioData class
│   ├── audio_io.py           # Load/save audio
│   ├── utils.py              # Helper functions
│   ├── processors.py         # Individual processors
│   └── processor.py          # Main AudioProcessor
├── examples.py               # Example usage
├── pyproject.toml            # Dependencies
└── README.md                 # This file
```

## License

MIT License

## Contributing

Contributions welcome! Feel free to fork and submit PRs.

---

**Made with ❤️ for audio enthusiasts**
