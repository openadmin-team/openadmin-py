# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from typing import Any

from openadmin import fastapi, spec

WEEKDAYS: list[dict[str, Any]] = [
    {"day": "Monday", "books": 5, "coffe": 5},
    {"day": "Tuesday", "books": 3, "coffe": 6},
    {"day": "Wednesday", "books": 7, "coffe": 7},
    {"day": "Thursday", "books": 9, "coffe": 8},
    {"day": "Friday", "books": 10, "coffe": 9},
]

page = fastapi.AdminPage("Week Days", icon="calendar", color="green")


@page.pie_chart(
    "How many books I have read 1",
    description="Books read per weekday, week 1",
    name_key="day",
    value_key="books",
    config={
        item["day"]: {
            "name": item["day"],
            "color": spec.COLORS[num + 10 % len(spec.COLORS)],
        }
        for num, item in enumerate(WEEKDAYS)
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
    caption="3 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
)
def get_books_2() -> spec.PieChart:
    return {
        "data": WEEKDAYS,
        "color": "amber",
        "icon": "a-arrow-up",
        "config": {
            item["day"]: {
                "name": item["day"],
                "color": spec.COLORS[num + 10 % len(spec.COLORS)],
            }
            for num, item in enumerate(WEEKDAYS)
        },
    }


@page.pie_chart(
    "How many books I have read 3",
    description="Books read per weekday, all pie chart options set",
    color="violet",
    icon="book-open",
    caption="5 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
    config={
        item["day"]: {
            "name": item["day"],
            "color": spec.COLORS[num + 10 % len(spec.COLORS)],
        }
        for num, item in enumerate(WEEKDAYS)
    },
)
def get_books_3() -> spec.PieChart:
    return [{"name": day["day"], "value": day["books"]} for day in WEEKDAYS]


@page.bar_chart(
    "Books & Coffee 1",
    description="Books read and coffee cups per weekday, week 1",
    data_key="day",
    config={
        "books": {"name": "Books", "color": "violet", "icon": "book-open"},
        "coffe": {"name": "Coffee", "color": "amber", "icon": "coffee"},
    },
    color="violet",
    icon="book-open",
    caption="5 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
)
def get_books_and_coffe_1() -> spec.BarChart:
    return WEEKDAYS


@page.bar_chart(
    "Books & Coffee 2",
    description="Books read and coffee cups per weekday, week 2",
    data_key="day",
    config={
        "books": {"name": "Books", "color": "violet", "icon": "book-open"},
        "coffe": {"name": "Coffee", "color": "amber", "icon": "coffee"},
    },
    color="amber",
    icon="a-arrow-up",
    caption="3 day streak",
    caption_description="Reading every day this work week",
    caption_icon="flame",
)
def get_books_and_coffe_2() -> spec.BarChart:
    return {
        "data": WEEKDAYS,
        "color": "amber",
        "icon": "a-arrow-up",
        "config": {
            "books": {"name": "Books", "color": "violet", "icon": "book-open"},
            "coffe": {"name": "Coffee", "color": "amber", "icon": "coffee"},
        },
    }
