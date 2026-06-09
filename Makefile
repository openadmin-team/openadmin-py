fix/format:
	@ uvx ruff format .

fix/lint:
	@ uvx ruff check --fix .

fix: fix/format fix/lint

check/format:
	@ uvx ruff format --check .

check/lint:
	@ uvx ruff check .

check/typing:
	@ uvx pyright .

check/cves:
	@ uv audit --preview-features audit

check/security:
	@ uvx bandit -r src -q

check/unused:
	@ uvx vulture src examples --min-confidence 80

check/spell:
	@ uvx codespell .

check/test:
	@ uvx pytest

check: check/format check/lint check/typing check/cves check/security check/unused check/spell check/test

dev/run:
	@ PYTHONPATH=. fastapi dev examples/main.py --reload