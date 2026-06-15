# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from .page_protocol import PageProtocol


class Section(BaseModel):
    name: str
    description: str | None
    pages: List[PageProtocol]
