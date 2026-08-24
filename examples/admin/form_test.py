from openadmin.fastapi import AdminPage
from openadmin import spec
from datetime import datetime

page = AdminPage("Test forms", icon='test-tube')

@page.form(
    'Test all fields',
    method='post',
    icon='university',
    color='green'
)
def get_info(
    string: str,
    int: int,
    float: float,
    date: datetime,
    bool: bool,
    list_of_strings: list[str],
    list_of_ints: list[str],
) -> spec.Form:
    return {
        'toast': f'All good ! {string=} {int=} {float=} {date=} {bool=} {list_of_ints=} {list_of_strings=}'
    }