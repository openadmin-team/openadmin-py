# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, NotRequired, Type, TypedDict

from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute


class Table(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    model: Type[DeclarativeBase]
    columns: NotRequired[List[InstrumentedAttribute]]
