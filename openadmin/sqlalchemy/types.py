# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import (
    Any,
    Awaitable,
    Callable,
    List,
    Literal,
    NotRequired,
    Tuple,
    Type,
    TypedDict,
)

from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute
from sqlalchemy.sql import Delete, Insert, Select, Update


class Table(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    model: Type[DeclarativeBase]
    query: NotRequired[Select]
    columns: NotRequired[List[InstrumentedAttribute]]
    actions: NotRequired[
        List[Literal["create", "delete", "update", "read"] | CustomAction]
    ]
    sort: NotRequired[List[InstrumentedAttribute]]


class CustomAction(TypedDict):
    name: str
    description: NotRequired[str]
    query: NotRequired[Callable[[Any], Update | Delete | Insert]]
    callback: NotRequired[Callable[[Any], Awaitable[Any]]]


class Stat(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    query: (
        Select[Tuple[int]]
        | Select[Tuple[str]]
        | Select[Tuple[float]]
        | Select[Tuple[bool]]
    )
