# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from .http_methods import HttpMethod
from .page import Page
from .section import Section
from .spec import Spec
from .stat import Stat
from .table import Stat as Table

__all__ = [
    "HttpMethod",
    "Page",
    "Section",
    "Spec",
    "Stat",
    "Table",
]
