# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass
from typing import Sequence

from .page_protocol import PageProtocol


@dataclass
class Section:
    name: str
    description: str | None
    pages: Sequence[PageProtocol]
