# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.fastapi import AdminPage
from openadmin.types import AreaChart, BarChart, LineChart, PieChart

page = AdminPage("Analytics")


@page.area_chart(
    "User Growth", description="New vs returning users over the last 6 months"
)
async def user_growth() -> AreaChart:
    return AreaChart(
        data=[
            {"month": "Jan", "new": 420, "returning": 1200},
            {"month": "Feb", "new": 380, "returning": 1350},
            {"month": "Mar", "new": 510, "returning": 1480},
            {"month": "Apr", "new": 670, "returning": 1620},
            {"month": "May", "new": 590, "returning": 1740},
            {"month": "Jun", "new": 740, "returning": 1890},
        ],
        config={
            "new": {"label": "New Users", "color": "hsl(var(--chart-1))"},
            "returning": {"label": "Returning Users", "color": "hsl(var(--chart-2))"},
        },
    )


@page.area_chart("Revenue Breakdown", description="Monthly revenue by plan tier")
async def revenue_breakdown() -> AreaChart:
    return AreaChart(
        data=[
            {"month": "Jan", "free": 0, "pro": 8400, "enterprise": 32000},
            {"month": "Feb", "free": 0, "pro": 9100, "enterprise": 34500},
            {"month": "Mar", "free": 0, "pro": 10200, "enterprise": 37000},
            {"month": "Apr", "free": 0, "pro": 11800, "enterprise": 41000},
            {"month": "May", "free": 0, "pro": 13400, "enterprise": 44500},
            {"month": "Jun", "free": 0, "pro": 15200, "enterprise": 49000},
        ],
        config={
            "free": {"label": "Free", "color": "hsl(var(--chart-3))"},
            "pro": {"label": "Pro", "color": "hsl(var(--chart-1))"},
            "enterprise": {"label": "Enterprise", "color": "hsl(var(--chart-2))"},
        },
    )


@page.area_chart("API Requests", description="Daily API call volume over the past week")
async def api_requests() -> AreaChart:
    return AreaChart(
        data=[
            {"day": "Mon", "requests": 142000},
            {"day": "Tue", "requests": 168000},
            {"day": "Wed", "requests": 195000},
            {"day": "Thu", "requests": 173000},
            {"day": "Fri", "requests": 210000},
            {"day": "Sat", "requests": 98000},
            {"day": "Sun", "requests": 74000},
        ],
        config={
            "requests": {"label": "API Requests", "color": "hsl(var(--chart-4))"},
        },
    )


@page.bar_chart(
    "Signups by Platform", description="Monthly signups split by desktop and mobile"
)
async def signups_by_platform() -> BarChart:
    return BarChart(
        data=[
            {"month": "January", "desktop": 186, "mobile": 80},
            {"month": "February", "desktop": 305, "mobile": 200},
            {"month": "March", "desktop": 237, "mobile": 120},
            {"month": "April", "desktop": 73, "mobile": 190},
            {"month": "May", "desktop": 209, "mobile": 130},
            {"month": "June", "desktop": 214, "mobile": 140},
        ],
        config={
            "desktop": {"label": "Desktop", "color": "hsl(var(--chart-1))"},
            "mobile": {"label": "Mobile", "color": "hsl(var(--chart-2))"},
        },
    )


@page.bar_chart(
    "Error Rate by Service",
    description="Average errors per day across backend services",
)
async def error_rate_by_service() -> BarChart:
    return BarChart(
        data=[
            {"service": "Auth", "errors": 12},
            {"service": "API", "errors": 43},
            {"service": "Storage", "errors": 7},
            {"service": "Queue", "errors": 29},
            {"service": "Mailer", "errors": 5},
        ],
        config={
            "errors": {"label": "Errors / day", "color": "hsl(var(--chart-3))"},
        },
    )


@page.line_chart("Page Views", description="Daily page views for the last two weeks")
async def page_views() -> LineChart:
    return LineChart(
        data=[
            {"date": "2026-05-19", "views": 2340},
            {"date": "2026-05-20", "views": 3120},
            {"date": "2026-05-21", "views": 2890},
            {"date": "2026-05-22", "views": 1540},
            {"date": "2026-05-23", "views": 1320},
            {"date": "2026-05-24", "views": 3450},
            {"date": "2026-05-25", "views": 3780},
            {"date": "2026-05-26", "views": 4100},
            {"date": "2026-05-27", "views": 3920},
            {"date": "2026-05-28", "views": 3670},
            {"date": "2026-05-29", "views": 2210},
            {"date": "2026-05-30", "views": 1980},
            {"date": "2026-05-31", "views": 4320},
            {"date": "2026-06-01", "views": 4550},
        ],
        config={
            "views": {"label": "Page Views", "color": "hsl(var(--chart-1))"},
        },
    )


@page.line_chart(
    "Response Time", description="Average API response time vs p99 over 6 months"
)
async def response_time() -> LineChart:
    return LineChart(
        data=[
            {"month": "January", "avg": 120, "p99": 340},
            {"month": "February", "avg": 132, "p99": 390},
            {"month": "March", "avg": 115, "p99": 310},
            {"month": "April", "avg": 148, "p99": 420},
            {"month": "May", "avg": 109, "p99": 290},
            {"month": "June", "avg": 124, "p99": 360},
        ],
        config={
            "avg": {"label": "Avg (ms)", "color": "hsl(var(--chart-2))"},
            "p99": {"label": "p99 (ms)", "color": "hsl(var(--chart-5))"},
        },
    )


@page.pie_chart(
    "Users by Plan", description="Distribution of users across subscription plans"
)
async def users_by_plan() -> PieChart:
    return PieChart(
        data=[
            {"plan": "free", "visitors": 1240},
            {"plan": "pro", "visitors": 530},
            {"plan": "enterprise", "visitors": 180},
        ],
        config={
            "visitors": {"label": "Users"},
            "free": {"label": "Free", "color": "hsl(var(--chart-1))"},
            "pro": {"label": "Pro", "color": "hsl(var(--chart-2))"},
            "enterprise": {"label": "Enterprise", "color": "hsl(var(--chart-3))"},
        },
    )


@page.pie_chart(
    "Traffic Sources", description="Where visitors are coming from this month"
)
async def traffic_sources() -> PieChart:
    return PieChart(
        data=[
            {"source": "organic", "visitors": 2750},
            {"source": "direct", "visitors": 1180},
            {"source": "referral", "visitors": 870},
            {"source": "social", "visitors": 640},
            {"source": "email", "visitors": 340},
        ],
        config={
            "visitors": {"label": "Visitors"},
            "organic": {"label": "Organic Search", "color": "hsl(var(--chart-1))"},
            "direct": {"label": "Direct", "color": "hsl(var(--chart-2))"},
            "referral": {"label": "Referral", "color": "hsl(var(--chart-3))"},
            "social": {"label": "Social", "color": "hsl(var(--chart-4))"},
            "email": {"label": "Email", "color": "hsl(var(--chart-5))"},
        },
    )
