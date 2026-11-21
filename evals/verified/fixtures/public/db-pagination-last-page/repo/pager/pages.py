import math


def page_count(total: int, per_page: int) -> int:
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    return max(1, math.ceil(total / per_page))


def page(items: list, number: int, per_page: int) -> list:
    """Items on 1-based page `number`."""
    if number < 1 or number > page_count(len(items), per_page):
        raise IndexError(number)
    start = (number - 1) * per_page
    end = start + per_page - 1
    return items[start:end]
