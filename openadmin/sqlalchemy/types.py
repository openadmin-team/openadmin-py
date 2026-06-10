# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import NotRequired, Type, TypedDict

from sqlalchemy.orm import DeclarativeBase


class Table(TypedDict):
    name: NotRequired[str]
    model: Type[DeclarativeBase]
