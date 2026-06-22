# Changelog

## [2.0.0] - 2026-06-22

### Changed
- Added proper Python package structure (`securityquest/`)
- Separated launcher CLI from game engine
- Extracted configuration and game registry

### Added
- `securityquest/` package with `__main__.py` entry point
- `securityquest/config.py` with centralized game registry
- `securityquest/cli.py` with Rich fallback for plain terminals
- 18 unit tests (config validation, engine, Cisco command matching)
- pyproject.toml, Makefile, CI pipeline, Dockerfile
- Documentation: ARCHITECTURE.md, USAGE.md
- Open source files: LICENSE, CONTRIBUTING, SECURITY, CHANGELOG
- GitHub Actions CI with test matrix (Python 3.10-3.13)

## [1.0.0] - 2026-06-20

### Added
- Initial release: 7 quests, 700 challenges
- Shared game engine with progress tracking and rank system
- Python exec, Bash exec, and Cisco command-match engines
