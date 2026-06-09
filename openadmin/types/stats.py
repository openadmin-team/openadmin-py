# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from pydantic import BaseModel


class Stat(BaseModel):
    value: str | bool | int | float
