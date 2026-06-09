# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any, Dict, List

from pydantic import BaseModel, Field, model_validator

from .actions import Action


class TableRow(BaseModel):
    model_config = {"extra": "allow", "populate_by_name": True}

    actions: List[Action] = Field(
        default=[],
        alias="__actions__",
        serialization_alias="__actions__",
    )


class Table(BaseModel):
    data: List[TableRow | Dict[str, Any]] = Field(default=[])

    @model_validator(mode="after")
    def coerce_rows(self) -> Table:
        """Coerce raw dicts into TableRow at runtime."""
        self.data = [
            TableRow.model_validate(row) if isinstance(row, dict) else row
            for row in self.data
        ]
        return self
