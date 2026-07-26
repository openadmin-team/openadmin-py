# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from .action import ActionComponent
from .area_chart import AreaChart
from .bar_chart import BarChartComponent
from .form import FormComponent
from .line_chart import LineChart
from .markdown import MarkdownComponent
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
    | ActionComponent
    | FormComponent
    | MarkdownComponent
)
