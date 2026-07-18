# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Protocol

from fastapi import FastAPI
from openadmin import spec


class PageProtocol(Protocol):
    def get_page_spec(self, app: FastAPI) -> spec.Page: ...
