from typing import TypedDict, NotRequired

class Error(TypedDict):
    message: str
    code: NotRequired[str]