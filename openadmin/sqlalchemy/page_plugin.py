# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.plugins import PagePlugin
from sqlalchemy.orm import DeclarativeBase


class SQLAlchemyPagePlugin(PagePlugin):
    def __init__(self, model: DeclarativeBase) -> None:
        self.model = model
