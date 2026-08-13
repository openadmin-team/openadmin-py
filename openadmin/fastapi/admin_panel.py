# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from pathlib import Path

from fastapi import APIRouter, FastAPI, HTTPException, status
from openadmin import spec

from . import deps, exc_handler, utils
from .admin_auth import AdminAuth
from .admin_page import AdminPage

_FRONTEND_DIR = Path(__file__).parent.parent / "__client__"


class AdminPanel:
    def __init__(
        self,
        name: str,
        *,
        description: str | None = None,
        auth: AdminAuth | None = None,
    ) -> None:
        self.version = "1.0.0"
        self.name = name
        self.description = description
        self.sections: list[spec.Section] = []
        self.auth = auth

        self.app = FastAPI(
            exception_handlers={
                HTTPException: exc_handler.http_exception_handler,
                Exception: exc_handler.app_exception_handler,
            },
        )
        self.frontend_router = APIRouter()
        self.api_router = APIRouter(
            dependencies=[deps.create_authenticate_dep(self.auth.authenticate_func)]
            if self.auth
            else None
        )
        self.auth_router = APIRouter()

        self.__mount_initial_routes()

    @property
    def spec(self) -> spec.Spec:
        return {
            "id": f"{utils.get_id(self.name)}",
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "sections": self.sections,
        }

    def section(
        self,
        name: str,
        *,
        description: str | None = None,
        icon: spec.Icon | None = None,
        pages: list[AdminPage],
    ) -> None:
        section_id = utils.get_id(name)

        self.sections.append(
            {
                "id": section_id,
                "name": name,
                "description": description,
                "icon": icon,
                "pages": [page.spec for page in pages],
            }
        )

        for page in pages:
            self.app.include_router(
                prefix=f"/{section_id}",
                router=page.router,
                tags=[name],
            )

    def __mount_initial_routes(self):
        self.api_router.get(
            "/openadmin.json",
            response_model=spec.Spec,
            summary="Get the OpenAdmin specification",
            description="Returns the OpenAdmin specification for this admin panel.",
        )(lambda: self.spec)

        self.frontend_router.frontend(
            "/", directory=str(_FRONTEND_DIR), fallback="index.html"
        )

        if self.auth:
            self.auth_router.post(
                "/login",
                status_code=status.HTTP_204_NO_CONTENT,
                summary="Log in",
                description="Log in user route",
            )(self.auth.login_func)
            self.auth_router.post(
                "/logout",
                status_code=status.HTTP_204_NO_CONTENT,
                summary="Log out",
                description="Log out user route",
                dependencies=[
                    deps.create_authenticate_dep(self.auth.authenticate_func)
                ],
            )(self.auth.logout_func)

        self.app.include_router(
            prefix="/auth",
            router=self.auth_router,
        )
        self.app.include_router(
            prefix="/api",
            router=self.api_router,
        )
        self.app.include_router(
            self.frontend_router,
        )
