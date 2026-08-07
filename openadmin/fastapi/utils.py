# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re
from collections.abc import Callable

from openadmin import spec

from . import counter

_SPECIAL_CHARS_RE = re.compile(r"[^a-zA-Z0-9\s]")


def get_id(seed: str) -> str:
    """Generate a unique ID based on a seed string."""
    kebab_name = _SPECIAL_CHARS_RE.sub("", seed).lower().replace(" ", "-")
    count = counter.inc(kebab_name)
    return kebab_name + (f"-{count}" if count != 0 else "")


def get_query_params(func: Callable) -> spec.JsonSchema | None: ...


def get_form_params(func: Callable) -> spec.JsonSchema | None: ...


def get_body_params(func: Callable) -> spec.JsonSchema | None: ...
