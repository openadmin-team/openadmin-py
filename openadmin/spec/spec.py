# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from .section import Section


class Spec(BaseModel):
    version: str
    name: str
    sections: List[Section]
