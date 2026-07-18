# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel, Field

from .property_type import PropertyType


class Property(BaseModel):
    name: str = Field(..., description="This name for showing to user in admin panel")
    alias: str = Field(..., description="This name goes to body or form for backend")
    type: PropertyType
    is_required: bool
    properties: List[Property] | None = Field(None)
