from app.cache import get_or_load, make_key

_ORGS = {7: {"kind": "org", "name": "Acme"}}


def load_profile(org_id: int) -> dict:
    return get_or_load(make_key("profile", org_id), lambda: dict(_ORGS[org_id]))
