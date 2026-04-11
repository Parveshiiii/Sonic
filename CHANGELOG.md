# Changelog

All notable changes to Audio Separation Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-11

### Added
- **Core Processors**
  - `AudioCropper` - Trim audio to specific time ranges
  - `AudioCombiner` - Blend two tracks with multiple methods (add, mean, subtract, multiply, divide)
  - `TempoShifter` - Change speed without pitch changes using phase vocoder
  - `TempoDetector` - Detect BPM using onset detection
  - `TempoMatcher` - Sync two tracks to average BPM
  - `AudioResampler` - Convert between sample rates

- **High-Level API**
  - `AudioProcessor` - Main orchestrator class with simple file-based methods
  - `AudioIO` - Load/save audio files with automatic format detection
  - `AudioUtils` - Helper functions (ensure_stereo, normalize, get_duration)

- **Data Structures**
  - `AudioData` - Standardized audio format with waveform and sample_rate

- **Features**
  - GPU acceleration with CUDA support
  - Batch processing for multiple operations
  - Auto device detection (GPU/CPU)
  - Comprehensive error handling
  - Detailed status messages

- **Documentation**
  - Complete README with quick start guide
  - API reference with examples
  - Architecture documentation
  - Contributing guidelines
  - 7 example scripts showing all features

- **Testing**
  - Test suite structure ready
  - Examples covering all major features

### Known Limitations
- Requires librosa for BPM detection (adds ~200MB to dependencies)
- Large files may require GPU for reasonable performance
- Audio longer than ~30 minutes may need chunking
- Some audio formats require ffmpeg installation

## Future Plans

### [0.2.0] - Planned
- [ ] Audio separation into stems (vocals, bass, drums, other) using Hybrid Demucs
- [ ] Video audio replacement functionality
- [ ] Advanced filtering (EQ, compressor)
- [ ] Real-time audio processing
- [ ] Streaming support for large files
- [ ] CLI tool with command-line interface
- [ ] Web API using FastAPI

### [0.3.0] - Planned
- [ ] Audio effects (reverb, delay, chorus)
- [ ] Pitch detection and correction
- [ ] Spectral analysis and visualization
- [ ] Multi-threaded batch processing
- [ ] WebAssembly support for browser

### Quality Improvements
- [ ] Increase test coverage to 95%+
- [ ] Performance benchmarking
- [ ] Memory optimization
- [ ] Parallel processing improvements

---

## How to Upgrade

### 0.1.0 (Current)
```bash
pip install audio-seperation==0.1.0
```

### From development
```bash
git clone https://github.com/yourusername/audio-seperation.git
cd audio-seperation
uv pip install -e .
```

---

**For latest updates, check [GitHub Releases](https://github.com/yourusername/audio-seperation/releases)**
