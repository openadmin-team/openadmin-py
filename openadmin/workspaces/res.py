from typing import TypedDict, NotRequired

class Workspace(TypedDict):
    id: str
    name: str
    avatar: NotRequired[str]
    description: NotRequired[str]