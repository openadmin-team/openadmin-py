# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from typing import Any

from openadmin import fastapi, spec

WEEKDAYS: list[dict[str, Any]] = [
    {"day": "Monday", "books": 5},
    {"day": "Tuesday", "books": 3},
    {"day": "Wednesday", "books": 7},
    {"day": "Thursday", "books": 9},
    {"day": "Friday", "books": 10},
]

page = fastapi.AdminPage(
    "Week Days",
    icon='calendar',
)


@page.pie_chart(
    "How many books I have read 1",
    description="Books read per weekday, week 1",
    name_key="day",
    value_key="books",
    config={
        "Monday": {
            "color": "amber",
            "icon": "sun",
        }
    },
    color="violet",
    icon="book-open",
    caption="5 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
)
def get_books_1() -> spec.PieChart:
    return WEEKDAYS


@page.pie_chart(
    "How many books I have read 2",
    description="Books read per weekday, week 2",
    name_key="day",
    value_key="books",
    config={
        item["day"]: {
            "name": item["day"],
            "color": spec.COLORS[num % len(spec.COLORS)],
        }
        for num, item in enumerate(WEEKDAYS)
    },
    color="amber",
    icon="air-vent",
    caption="3 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
)
def get_books_2() -> spec.PieChart:
    return WEEKDAYS


@page.pie_chart(
    "How many books I have read 3",
    description="Books read per weekday, all pie chart options set",
    name_key="day",
    value_key="books",
    color="violet",
    icon="book-open",
    caption="5 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
    config={
        item["day"]: {
            "name": item["day"],
            "color": spec.COLORS[num % len(spec.COLORS)],
        }
        for num, item in enumerate(WEEKDAYS)
    },
)
def get_books_3() -> spec.PieChart:
    return WEEKDAYS
