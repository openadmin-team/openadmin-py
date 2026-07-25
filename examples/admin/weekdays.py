# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from openadmin import fastapi, spec

WEEKDAYS = [
    {"day": "Monday", "books": 5},
    {"day": "Tuesday", "books": 3},
    {"day": "Wednesday", "books": 7},
    {"day": "Thursday", "books": 9},
    {"day": "Friday", "books": 10},
]

page = fastapi.AdminPage("Week Days")


@page.pie_chart(
    "How many books I have read 1",
    name_key="day",
    value_key="books",
    config={
        "Monday": {
            "color": "amber",
            "icon": "sun",
        }
    },
)
def get_books_1() -> spec.PieChart:
    return WEEKDAYS


@page.pie_chart(
    "How many books I have read 2",
)
def get_books_2() -> spec.PieChart:
    return {
        "data": WEEKDAYS,
        "color": "amber",
        "icon": "air-vent",
        "config": {
            item["day"]: {
                "name": item["day"],
                "color": spec.COLORS[num % len(spec.COLORS)],
            }
            for num, item in enumerate(WEEKDAYS)
        },
    }
