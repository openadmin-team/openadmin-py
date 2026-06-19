# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable

from pydantic import BaseModel, ConfigDict

from openadmin import spec


class AreaChart(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    function_name: str
    name: str
    description: str | None
    method: spec.HttpMethod
    func: Callable | None = None
