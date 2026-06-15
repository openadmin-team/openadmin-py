# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Union

from .area_chart import AreaChart
from .bar_chart import BarChart
from .line_chart import LineChart
from .pie_chart import PieChart
from .stat import Stat
from .table import Stat as Table

type Component = Union[Stat, Table, AreaChart, BarChart, LineChart, PieChart]
