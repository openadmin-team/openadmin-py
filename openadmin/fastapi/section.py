# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Sequence
from dataclasses import dataclass

from openadmin import spec

from .page_protocol import PageProtocol


@dataclass
class Section:
    id: str
    name: str
    description: str | None
    icon: spec.Icon | None
    pages: Sequence[PageProtocol]
