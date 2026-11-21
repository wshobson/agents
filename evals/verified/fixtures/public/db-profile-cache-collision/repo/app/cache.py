_store: dict[str, object] = {}


def make_key(*parts: object) -> str:
    return ":".join(str(p) for p in parts)


def get_or_load(key: str, loader):
    if key not in _store:
        _store[key] = loader()
    return _store[key]


def clear() -> None:
    _store.clear()
