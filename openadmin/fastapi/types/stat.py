# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic import BaseModel

from openadmin import spec


class Stat(BaseModel):
    function_name: str
    method: spec.HttpMethod
    name: str
    description: str | None
