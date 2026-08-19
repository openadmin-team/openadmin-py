#
# Fix
#

fix/license:
	@ uv run reuse download --all
	@ uv run reuse annotate --license AGPL-3.0-or-later --copyright "OpenAdmin" --recursive --skip-unrecognised openadmin/
	@ uv run reuse annotate --license AGPL-3.0-or-later --copyright "OpenAdmin" --recursive --skip-unrecognised tests/
	@ uv run reuse annotate --license AGPL-3.0-or-later --copyright "OpenAdmin" --recursive --skip-unrecognised examples/
	@ uv run reuse annotate --license AGPL-3.0-or-later --copyright "OpenAdmin" --recursive --skip-unrecognised $$(find client/src -mindepth 1 -maxdepth 1 ! -name assets)

fix/format:
	@ cd client && bun run fix:format
	@ uv run ruff format .

fix/lint:
	@ cd client && bun run fix:lint
	@ uv run ruff check --fix .

fix: fix/license fix/format fix/lint

#
# Check
#

check/format:
	@ cd client && bun run check:format
	@ uv run ruff format --check .

check/lint:
	@ cd client && bun run check:lint
	@ uv run ruff check .

check/typing:
	@ cd client && bun run check:types
	@ uv run pyright .

check/cves:
	@ uv audit --preview-features audit

check/security:
	@ uv run bandit -r openadmin -q

check/unused:
	@ uv run vulture openadmin --min-confidence 80

check/spell:
	@ uv run codespell .

check/license:
	@ uv run reuse lint

check/test:
	@ uv run pytest

check: check/format check/lint check/typing check/cves check/security check/unused check/spell check/license check/test

#
# Dev
#

dev/client:
	@ cd client && bun run dev

dev/docs:
	@ cd docs && bun run dev

dev/example:
	@ cd client && bun run build
	@ PYTHONPATH=. uv run fastapi dev examples/main.py --host 0.0.0.0 --port $${PORT:-8000} --reload
