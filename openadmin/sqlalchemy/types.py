# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Awaitable, Callable
from typing import (
    Any,
    Literal,
    NotRequired,
    TypedDict,
)

from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute
from sqlalchemy.sql import Delete, Insert, Select, Update


class Table(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    model: type[DeclarativeBase]
    query: NotRequired[Select]
    columns: NotRequired[list[InstrumentedAttribute]]
    actions: NotRequired[
        list[Literal["create", "delete", "update", "read"] | Action]
    ]
    sort: NotRequired[list[InstrumentedAttribute]]


class Action(TypedDict):
    name: str
    description: NotRequired[str]
    query: NotRequired[Callable[[Any], Update | Delete | Insert]]
    callback: NotRequired[Callable[[Any], Awaitable[Any]]]


class Stat(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    query: (
        Select[tuple[int]]
        | Select[tuple[str]]
        | Select[tuple[float]]
        | Select[tuple[bool]]
    )
