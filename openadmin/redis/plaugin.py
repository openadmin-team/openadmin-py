# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.plugins import PagePlugin


class RedisPlugin(PagePlugin):
    def __init__(self, prefix: str | None = None):
        self.prefix = prefix
