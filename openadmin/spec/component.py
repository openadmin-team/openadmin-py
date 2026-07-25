# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from .action import Action
from .area_chart import AreaChart
from .bar_chart import BarChartComponent
from .form import Form
from .line_chart import LineChart
from .markdown import Markdown
from .pie_chart import PieChartComponent
from .stat import StatComponent
from .table import TableComponent

type Component = (
    StatComponent
    | TableComponent
    | AreaChart
    | BarChartComponent
    | LineChart
    | PieChartComponent
    | Action
    | Form
    | Markdown
)
