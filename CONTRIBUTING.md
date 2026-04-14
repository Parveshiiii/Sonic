# Contributing to Audio Separation Library

Thank you for your interest in contributing! Here's how you can help.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/Parveshiiii/Sonic.git
   cd audio-seperation
   ```

2. **Set up development environment**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints for all function parameters and returns
- Write docstrings for all public functions and classes
- Maximum line length: 100 characters

### Testing
- Write tests for new features
- Run tests before submitting PR:
  ```bash
  pytest tests/
  ```
- Aim for >90% code coverage

### Commit Messages
```
# Format: [TYPE] Brief description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Tests
- refactor: Code refactoring
- perf: Performance improvement

Example:
feat: Add audio filtering capabilities
fix: Handle mono audio in TempoDetector
docs: Add API reference for processors
```

## Pull Request Process

1. **Before submitting:**
   - Update documentation
   - Add tests for new features
   - Ensure all tests pass
   - Update CHANGELOG.md if applicable

2. **PR description should include:**
   - What changes are made
   - Why they're needed
   - How to test them
   - Any breaking changes

3. **Code review:**
   - Maintainers will review your code
   - Address feedback or discuss concerns
   - Once approved, your PR will be merged

## Reporting Issues

### Bug Reports
Include:
- Python version
- Library version
- Steps to reproduce
- Expected vs actual behavior
- Error traceback

### Feature Requests
Include:
- Use case/motivation
- Proposed API/design
- Example code snippet

## Documentation

- Keep README.md up-to-date
- Update docstrings with changes
- Add examples for new features
- Document breaking changes in CHANGELOG.md

## Questions?

- Open a GitHub Discussion
- Check existing Issues for similar questions
- Read the docs in `/docs` folder

## License

By contributing, you agree your code will be licensed under MIT License.

---

**Thank you for contributing! 🎵**
