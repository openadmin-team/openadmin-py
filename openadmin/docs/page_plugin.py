# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

from openadmin.plugins import AdminPageProtocol, PagePlugin


class DocsPagePlugin(PagePlugin):
    def __init__(self, path: Path) -> None:
        self.path = path

    def after_page_init(self, page: AdminPageProtocol) -> None:
        if self.path.is_file():
            handler = self.__create_docs_file_route(self.path)
            page.markdown(self.path.stem)(handler)
        else:
            files = [f for f in self.path.iterdir() if f.is_file()]
            for file in files:
                handler = self.__create_docs_file_route(file)
                page.markdown(file.stem)(handler)

    def __create_docs_file_route(self, file: Path):
        with open(file, "r") as f:
            text = f.read()

        def route():
            return text

        return route
