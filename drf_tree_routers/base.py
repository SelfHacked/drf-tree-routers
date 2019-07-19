import typing as _typing

from django.urls import (
    path as _path,
    include as _include,
)
from rest_framework.decorators import (
    api_view as _api_view,
)
from rest_framework.response import (
    Response as _Response,
)
from returns import (
    returns as _returns,
)

from .util import cached_property


class AbstractTreeRouter(object):
    def __init__(self):
        self._nested: _typing.Dict[str, 'AbstractTreeRouter'] = {}

    def __getitem__(self, route: str) -> 'AbstractTreeRouter':
        return self._nested[route]

    def __setitem__(self, route: str, router: 'AbstractTreeRouter'):
        self._nested[route] = router

    def _get_self_urls(self) -> _typing.Iterator:
        raise NotImplementedError

    def _get_nested_urls(self) -> _typing.Iterator:
        for route, router in self._nested.items():
            yield _path(
                route,
                _include(router.urls),
            )

    @property  # type: ignore
    @_returns(list)
    def urls(self) -> list:
        yield from self._get_self_urls()
        yield from self._get_nested_urls()

    def __iter__(self) -> _typing.Iterator[_typing.Tuple[str, _typing.Any]]:
        for route, router in self._nested.items():
            yield route, dict(router)


class TreeRouter(AbstractTreeRouter):
    """Tree router that accepts a single view."""

    def __init__(
            self,
            *,
            view,
            name: str,
            **kwargs,
    ):
        super().__init__()
        self.__view = view
        self.__name = name
        self.__kwargs = kwargs

    def _get_self_urls(self) -> _typing.Iterator:
        yield _path(
            '',
            view=self.__view,
            name=self.__name,
            **self.__kwargs,
        )

    def __iter__(self) -> _typing.Iterator[_typing.Tuple[str, _typing.Any]]:
        yield '', self.__name
        yield from super().__iter__()


class RootRouter(AbstractTreeRouter):
    """Root tree router."""

    def __init__(self, *, root_prefix='/'):
        """Initialize root router."""
        super().__init__()
        self.__root_prefix = root_prefix

    @cached_property
    def _view(self):
        def _clean(d, prefix):
            if isinstance(d, str):
                return d
            if '' in d and len(d) == 1:
                return _clean(d[''], prefix)

            result = []
            for i, k in enumerate(d):
                route = f'{prefix}{k}'
                v = _clean(d[k], route)
                if isinstance(v, str):
                    result.append(route)
                else:
                    result.append(v)
            return result

        @_api_view()
        def get(request):
            """List all endpoints as tree."""
            return _Response(_clean(dict(self), self.__root_prefix))

        return get

    def _get_self_urls(self) -> _typing.Iterator:
        yield _path(
            '',
            view=self._view,
        )
