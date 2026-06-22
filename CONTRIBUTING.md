# Contributing to SecurityQuestAcademy

## Development Setup

```bash
git clone https://github.com/arkanzasfeziii/SecurityQuestAcademy.git
cd SecurityQuestAcademy
pip install -r requirements.txt
pip install -r requirements-dev.txt
make test
```

## Adding a New Quest

1. Create `games/yourquest.py` using `games/base.py` engine
2. Define levels as a list of dicts with: id, title, category, points, description, challenge, hint, test_code
3. Register in `securityquest/config.py` under `GAMES`
4. Add tests in `tests/`

## Adding Challenges to an Existing Quest

Each quest contains a `LEVELS` list. Add new level dicts following the existing pattern. Each level needs: a unique id, test assertion code, and a hint.

## Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/):
```
feat(cryptoquest): add post-quantum cryptography levels
fix(engine): handle multiline Python input correctly
docs: update quest descriptions
```
