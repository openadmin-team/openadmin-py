# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from pydantic import BaseModel

from openadmin import spec


class LineChart(BaseModel):
    function_name: str
    name: str
    description: str | None
    url: str
    method: spec.HttpMethod
