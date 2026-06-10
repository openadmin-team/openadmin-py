# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from openadmin.plugins import PanelPlugin

from .state import PluginSharedState


class SQLAlchemyPanelPlugin(PanelPlugin):
    def __init__(
        self,
    ):
        self.shared_state: PluginSharedState = {}
