from app.cache import get_or_load, make_key

_USERS = {7: {"kind": "user", "name": "Ada"}, 8: {"kind": "user", "name": "Lin"}}


def load_profile(user_id: int) -> dict:
    return get_or_load(make_key("profile", user_id), lambda: dict(_USERS[user_id]))
