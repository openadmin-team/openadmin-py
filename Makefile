fix/license:
	@ uvx "reuse[charset-normalizer]" download --all
	@ uvx "reuse[charset-normalizer]" annotate --license AGPL-3.0-or-later --recursive --skip-unrecognised openadmin/
	@ uvx "reuse[charset-normalizer]" annotate --license AGPL-3.0-or-later --recursive --skip-unrecognised tests/
	@ uvx "reuse[charset-normalizer]" annotate --license AGPL-3.0-or-later --recursive --skip-unrecognised examples/

fix/format:
	@ uvx ruff format .

fix/lint:
	@ uvx ruff check --fix .

fix: fix/license fix/format fix/lint

check/format:
	@ uvx ruff format --check .

check/lint:
	@ uvx ruff check .

check/typing:
	@ uvx pyright .

check/cves:
	@ uv audit --preview-features audit

check/security:
	@ uvx bandit -r openadmin -q

check/unused:
	@ uvx vulture openadmin --min-confidence 80

check/spell:
	@ uvx codespell .

check/license:
	@ uvx "reuse[charset-normalizer]" lint

check/test:
	@ uvx pytest

check: check/format check/lint check/typing check/cves check/security check/unused check/spell check/license check/test

dev/run:
	@ PYTHONPATH=. fastapi dev examples/main.py --reload