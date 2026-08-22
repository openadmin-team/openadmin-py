# Authentication

`AdminAuth` holds three hooks — login, authenticate, and logout — and `AdminPanel` wires them into the panel's routes for you.

```python
from openadmin.fastapi import AdminAuth

auth = AdminAuth()
```

::: warning No protection by default
An `AdminAuth()` instance's three hooks are no-op stubs until you override them: `login` and `logout` do nothing, and `authenticate` never raises — so it lets every request through. Passing `auth=None` to `AdminPanel` (the default) is equivalent: no `/auth/*` routes are even mounted, and `/api/*` is completely open. Either way, nothing is actually gated until you decorate all three hooks yourself.
:::

## The three hooks

```python
@auth.login()
def login(req: Request, login_req: LoginReq) -> None: ...


@auth.authenticate()
def authenticate(req: Request) -> None: ...


@auth.logout()
def logout(req: Request) -> None: ...
```

Each decorator just stores the function you give it — it doesn't wrap or alter it, so the function can still be called or tested directly like any other. Each hook may be sync or async (`None | Awaitable[None]`).

- **`login_func(req, login_req)`** — receives a `LoginReq` (`{username: str, password: str}`, a pydantic model). Raise an `HTTPException` to reject the credentials; return normally to accept them. This is where you'd typically write something into `req.session`.
- **`authenticate_func(req)`** — runs as a dependency on **every** request under `/api/*`, i.e. every stat, table, form, action, chart, and markdown endpoint on every page. Raise an `HTTPException` (typically 401) to reject the request; return normally to allow it.
- **`logout_func(req)`** — typically clears `req.session`. It runs behind `authenticate_func` itself, so a caller must already be authenticated to log out.

## How `AdminPanel` wires them up

Passing `auth=` to `AdminPanel(...)` does three things:

1. Mounts `POST /auth/login`, calling your `login_func` and returning `204 No Content` on success.
2. Mounts `POST /auth/logout`, calling your `logout_func`, itself gated behind `authenticate_func`.
3. Adds `authenticate_func` as a router-level dependency on the entire `/api` router — so it runs before any component endpoint, panel-wide, with no per-page or per-component opt-in needed.

The frontend's static assets (served at `/`) and the login endpoint itself are intentionally not gated, since a client needs to load the login screen and call `/auth/login` before it has anything to authenticate with.

## Example

```python
# admin/auth.py
from fastapi import HTTPException, Request, status

from openadmin.fastapi import AdminAuth, LoginReq

auth = AdminAuth()


@auth.login()
def login(req: Request, login_req: LoginReq) -> None:
    if login_req.username == "admin" and login_req.password == "admin":
        req.session.update({"token": "admin-token"})
    else:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid username or password"
        )


@auth.authenticate()
def authenticate(req: Request) -> None:
    if req.session.get("token") != "admin-token":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


@auth.logout()
def logout(req: Request) -> None:
    req.session.clear()
```

`req.session` comes from Starlette's `SessionMiddleware`, added on the *outer* application — not on `admin.app` — since middleware on the outer app also covers requests routed into the mounted sub-app:

```python
# main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from openadmin.fastapi import AdminPanel

from .admin.auth import auth

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="change-me")

admin = AdminPanel("My Admin", auth=auth)
app.mount("/admin", admin.app)
```

::: danger
Cookie-based sessions are only as secure as `secret_key`. Never hardcode it — load it from an environment variable or secret store — and compare credentials with a real user store and hashed passwords, not the plaintext check shown above.
:::

See [Implementing Auth](/cookbook/implementing-auth) for a full step-by-step recipe.
