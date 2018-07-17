from typing import Callable, Union


def before_validation(order: Union[Callable, int]):

    if callable(order):
        order.__vang_before__ = 0
        return order

    def decorator(method):
        method.__vang_before__ = order
        return method

    return decorator


def after_validation(order: Union[Callable, int]):

    if callable(order):
        order.__vang_after__ = 0
        return order

    def decorator(method):
        method.__vang_after__ = order
        return method

    return decorator
