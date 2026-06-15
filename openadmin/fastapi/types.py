# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Protocol

from pydantic import BaseModel

from fastapi import FastAPI
from openadmin import spec


class Stat(BaseModel):
    function_name: str
    method: spec.HttpMethod
    name: str
    description: str | None


class Table(BaseModel):
    function_name: str
    method: spec.HttpMethod
    name: str
    description: str | None


class PageProtocol(Protocol):
    def get_page_spec(self, app: FastAPI) -> spec.Page: ...


class Section(BaseModel):
    name: str
    description: str | None
    pages: List[PageProtocol]
