# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from pydantic import BaseModel

from openadmin.fastapi import AdminPage

page = AdminPage("Users Managment")


class User(BaseModel):
    email: str
    username: str


class CreateUserReq(User): ...


users: List[User] = []


@page.stat("User count")
async def user_count() -> int:
    return len(users)


@page.table("Users table")
async def users_table() -> List[User]:
    return users


@page.form_post("Create user")
async def create_user(user: CreateUserReq) -> None:
    users.append(User(email=user.email, username=user.username))
    return None
