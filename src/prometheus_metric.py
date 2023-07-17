from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable, Callable

if TYPE_CHECKING:
    from prometheus_async.types import Incrementer, P, R, T

from wrapt import decorator

from typing import Any

from prometheus_client import Counter

language_metrics = {'en': Counter('en', 'count en language'),
                    'ru': Counter('ru', 'count ru language')}


def count_language(
        metric: Incrementer,
        future: Awaitable[T] | None = None,
        *,
        exc: type[BaseException] = BaseException,
) -> Callable[[Callable[P, R]], Callable[P, R]] | Awaitable[T]:
    r"""
    Call ``metric.inc()`` whenever *exc* is caught.

    Works as a decorator as well as on :class:`asyncio.Future`\ s.

    :returns: coroutine function (if decorator) or coroutine.
    """

    if future is None:

        @decorator
        async def count(
                wrapped: Callable[..., R], _: Any, args: Any, kw: Any
        ) -> R:
            print("key ", kw)
            try:
                metric[kw['language']].inc()
            except Exception as e:
                print("No such language:", e)
            rv = await wrapped(*args, **kw)
            return rv

        return count
    else:
        f = future
        print("f", f)

        async def count() -> T:
            print("locals", locals())

            rv = await f
            return rv

        return count()
