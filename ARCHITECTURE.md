# Architecture: Processor vs Processors

## Separation of Concerns

The library intentionally separates two layers:

### 1. **processors.py** - Core Processing Layer
```
Raw Audio Data (AudioData) → Processing Logic → Processed Audio Data
```

**Contains:**
- `AudioCropper` - Core cropping logic
- `AudioCombiner` - Core combining logic
- `TempoShifter` - Core time-shifting (phase vocoder)
- `TempoDetector` - Core BPM detection
- `TempoMatcher` - Core tempo matching
- `AudioResampler` - Core resampling

**Characteristics:**
- Works with `AudioData` objects (in-memory tensors)
- Pure processing functions
- No file I/O
- Stateless (can chain operations)
- Low-level API

**Use when:** You already have audio loaded and want direct control

```python
from sonic.processors import AudioCropper
from sonic.audio_io import AudioIO

# Direct use
audio = AudioIO.load("song.wav")
cropped = AudioCropper.crop(audio, 30, 90)
AudioIO.save(cropped, "output.wav")
```

---

### 2. **processor.py** - High-Level Orchestration Layer
```
File Path → Load → Process → Save → File Path
```

**Contains:**
- `AudioProcessor` - Main orchestrator class

**Characteristics:**
- Works with file paths (strings)
- Handles file I/O automatically
- Manages device (GPU/CPU)
- Convenient API for common tasks
- High-level API
- Prints status messages

**Use when:** You want simple file operations without manual I/O

```python
from sonic.processor import AudioProcessor

# Simple file-based workflow
processor = AudioProcessor(device="cuda")
processor.crop("song.wav", "output.wav", 30, 90)
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          User Code / CLI / Application              │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│  processor.py - AudioProcessor (High-Level API)     │
│  - crop(file, output, ...)                          │
│  - combine(file1, file2, output, ...)               │
│  - speed_change(file, output, ...)                  │
│  - detect_bpm(file)                                 │
│  - match_tempo(...)                                 │
│  - resample(...)                                    │
│  - batch_process(...)                               │
└─────────────────────────────────────────────────────┘
        ↓ Loads Audio    ↓ Saves Audio
┌─────────────────────────────────────────────────────┐
│  audio_io.py - AudioIO (I/O Layer)                  │
│  - load(file_path, device)                          │
│  - save(audio, output_path)                         │
└─────────────────────────────────────────────────────┘
        ↓ Uses              ↓ Creates
┌─────────────────────────────────────────────────────┐
│  processors.py - Core Processors (Low-Level API)    │
│  - AudioCropper.crop()                              │
│  - AudioCombiner.combine()                          │
│  - TempoShifter.shift()                             │
│  - TempoDetector.detect_bpm()                       │
│  - TempoMatcher.match()                             │
│  - AudioResampler.resample()                        │
└─────────────────────────────────────────────────────┘
        ↓ Operates On
┌─────────────────────────────────────────────────────┐
│  types.py - AudioData (Data Structure)              │
│  - waveform: torch.Tensor                           │
│  - sample_rate: int                                 │
└─────────────────────────────────────────────────────┘
```

---

## Two-Layer API

### Layer 1: High-Level (Easy, File-Based)

```python
from sonic.processor import AudioProcessor

processor = AudioProcessor()
processor.crop("input.wav", "output.wav", 30, 90)
```

✅ Simple  
✅ Automatic file loading/saving  
✅ Perfect for CLI tools and simple scripts  
❌ Less control over individual steps  

---

### Layer 2: Low-Level (Flexible, Data-Based)

```python
from sonic.processors import AudioCropper
from sonic.audio_io import AudioIO

audio = AudioIO.load("input.wav")
cropped = AudioCropper.crop(audio, 30, 90)
AudioIO.save(cropped, "output.wav")
```

✅ Direct control  
✅ Can chain operations  
✅ Can work with in-memory data  
❌ More boilerplate code  

---

## When to Use Each

| Use Case | Layer |
|----------|-------|
| CLI tool / simple batch processing | High-level (`AudioProcessor`) |
| GUI application | High-level for buttons/workflows |
| Data pipeline / batch jobs | Either (depends on workflow) |
| Research / experimentation | Low-level (`processors`) |
| Advanced workflows | Low-level + combine custom logic |
| One-off operations | High-level |

---

## Migration Path

If you need to switch layers:

### From High-Level to Low-Level

```python
# This:
processor = AudioProcessor()
processor.crop("in.wav", "out.wav", 30, 90)

# Becomes:
from sonic.processors import AudioCropper
from sonic.audio_io import AudioIO

audio = AudioIO.load("in.wav")
cropped = AudioCropper.crop(audio, 30, 90)
AudioIO.save(cropped, "out.wav")
```

### From Low-Level to High-Level

```python
# This:
audio = AudioIO.load("in.wav")
cropped = AudioCropper.crop(audio, 30, 90)
AudioIO.save(cropped, "out.wav")

# Becomes:
processor = AudioProcessor()
processor.crop("in.wav", "out.wav", 30, 90)
```

---

## Summary

✅ **They ARE properly separated**  
✅ **This is the correct architecture**  
✅ **No duplication - different purposes**  

- `processors.py` = **Core Logic** (reusable, testable)
- `processor.py` = **Convenience Wrapper** (user-friendly, file-based)
