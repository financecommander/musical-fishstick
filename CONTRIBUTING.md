# Contributing to EdgeForge

Thank you for your interest in contributing to EdgeForge!

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/musical-fishstick.git
cd musical-fishstick
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Document all public APIs
- Write unit tests for new features

Format your code:
```bash
black edgeforge/
isort edgeforge/
```

Lint your code:
```bash
flake8 edgeforge/
mypy edgeforge/
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add tests
4. Update documentation
5. Run tests and linters
6. Submit PR with clear description

## Development Strategy

EdgeForge uses a poly-agent development workflow:

### Grok Code Fast 1 (Primary - 80%)
- DSL syntax and API design
- Code generation and scaffolding
- Build tooling and CI/CD
- Deployment infrastructure
- Integration code

### Claude Sonnet 4.5 (Optimization - 20%)
- Quantization algorithms
- Pruning strategies
- Memory management
- Performance-critical kernels
- Numerical stability

## Testing

Add tests for all new features:
```python
# tests/test_my_feature.py
def test_my_feature():
    # Your test here
    pass
```

Run specific tests:
```bash
pytest tests/test_my_feature.py -v
```

## Documentation

Update documentation for:
- New features
- API changes
- Examples
- Configuration options

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions
- Discussions
