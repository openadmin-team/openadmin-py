# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("Users Management")


class ShopList(BaseModel):
    product_name: str


class Performance(BaseModel):
    good: bool


class User(BaseModel):
    email: str
    username: str
    names: List[str]
    shop_list: List[ShopList]
    performance: Performance


users: List[User] = []


@page.stat("User count")
async def user_count() -> int:
    return len(users)


@page.table("Users table")
async def users_table() -> List[User]:
    return users


@page.form_post("Create user")
async def create_user(user: User) -> None:
    users.append(user)
    return None
