# Implementing Auth

A step-by-step recipe for gating a panel behind a login screen. Background on how the pieces fit together is in [Authentication](/auth/).

## 1. Add session support to the outer app

OpenAdmin doesn't ship a session store — use Starlette's `SessionMiddleware`, added to the app you mount the panel onto (not to `admin.app` itself):

```python
# main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_SECRET"])
```

## 2. Create an `AdminAuth` instance

```python
# admin/auth.py
from openadmin.fastapi import AdminAuth

auth = AdminAuth()
```

## 3. Implement login

Validate credentials against your real user store, then write a session marker:

```python
from fastapi import HTTPException, Request, status

from openadmin.fastapi import LoginReq
from .users import verify_password, get_user_by_username


@auth.login()
async def login(req: Request, login_req: LoginReq) -> None:
    user = await get_user_by_username(login_req.username)
    if user is None or not verify_password(login_req.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid username or password"
        )

    req.session["user_id"] = user.id
```

`LoginReq` is a pydantic model with `username: str` and `password: str`. Raising `HTTPException` here is what makes `POST /auth/login` return an error instead of `204`.

## 4. Implement authenticate

This runs before every request under `/api/*`, so keep it cheap — a session lookup, not a full user fetch, if you can avoid it:

```python
@auth.authenticate()
def authenticate(req: Request) -> None:
    if "user_id" not in req.session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
```

## 5. Implement logout

```python
@auth.logout()
def logout(req: Request) -> None:
    req.session.clear()
```

## 6. Wire it into the panel

```python
# admin/panel.py
from openadmin.fastapi import AdminPanel

from .auth import auth

admin = AdminPanel("My Admin", auth=auth)
```

At this point every `/api/*` call — every stat, table, form, and action on every page — requires a valid session, and `/admin/` still serves the frontend so a logged-out visitor can reach the login screen at all.

## Alternative: token-based auth

`authenticate_func` just receives the `Request`, so nothing ties you to cookies. To check a bearer token instead:

```python
@auth.authenticate()
def authenticate(req: Request) -> None:
    token = req.headers.get("authorization", "").removeprefix("Bearer ")
    if not is_valid_token(token):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
```

In that case `login_func` can simply be left as a no-op (or removed from your flow entirely) if tokens are issued out of band, since nothing requires you to use `/auth/login` at all.
