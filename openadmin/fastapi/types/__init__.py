# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Union

from .action import Action
from .area_chart import AreaChart
from .bar_chart import BarChart
from .form import Form
from .line_chart import LineChart
from .page_protocol import PageProtocol
from .pie_chart import PieChart
from .section import Section
from .stat import Stat
from .table import Table

type Component = Union[
    Stat, Table, AreaChart, BarChart, LineChart, PieChart, Action, Form
]

__all__ = [
    "PageProtocol",
    "Section",
    "Stat",
    "Table",
    "Action",
    "AreaChart",
    "BarChart",
    "Form",
    "LineChart",
    "PieChart",
    "Component",
]
