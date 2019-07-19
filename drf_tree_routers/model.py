import typing as _typing

from django.urls import (
    path as _path,
    include as _include,
)

from .base import (
    AbstractTreeRouter as _AbstractTreeRouter,
)
from .util import cached_property


class ModelTreeRouter(_AbstractTreeRouter):
    """Tree router that accepts a view set."""

    LIST_ACTIONS: dict = {
        'get': 'list',
        'post': 'create',
    }
    DETAIL_ACTIONS: dict = {
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }

    def __init__(
            self,
            *,
            viewset,
            name: str,
    ):
        super().__init__()
        self.__viewset = viewset
        self.__name = name

    @property
    def _viewset(self):
        return self.__viewset

    @property
    def _name(self) -> str:
        return self.__name

    @cached_property
    def _lookup(self) -> str:
        result = (
                getattr(self._viewset, 'lookup_url_kwarg', None) or
                getattr(self._viewset, 'lookup_field', None)
        )
        if result and result != 'pk':
            return result

        raise ValueError(
            f'{self._viewset.__name__} must have `lookup_url_kwargs` '
            'or `lookup_field` specified, '
            "and must not be 'pk'.",
        )

    @property
    def _detail_route(self) -> str:
        return f'<{self._lookup}>/'

    @property
    def _list_view(self):
        return self._viewset.as_view(actions=self.LIST_ACTIONS)

    @property
    def _list_view_name(self) -> str:
        return f'{self._name}-list'

    @property
    def _detail_view(self):
        return self._viewset.as_view(actions=self.DETAIL_ACTIONS)

    @property
    def _detail_view_name(self) -> str:
        return f'{self._name}-detail'

    def _get_self_urls(self) -> _typing.Iterator:
        if self.LIST_ACTIONS:
            yield _path(
                '',
                view=self._list_view,
                name=self._list_view_name,
            )
        if self.DETAIL_ACTIONS:
            yield _path(
                self._detail_route,
                view=self._detail_view,
                name=self._detail_view_name,
            )

    def _get_nested_urls(self) -> _typing.Iterator:
        yield _path(
            self._detail_route,
            _include(list(super()._get_nested_urls())),
        )

    def __iter__(self) -> _typing.Iterator[_typing.Tuple[str, _typing.Any]]:
        if self.LIST_ACTIONS:
            yield '', self._list_view_name
        detail = {}
        if self.DETAIL_ACTIONS:
            detail[''] = self._detail_view_name
        detail.update(super().__iter__())
        yield self._detail_route, detail


class OneToOneModelTreeRouter(ModelTreeRouter):
    """Tree router for one-to-one related model."""

    LIST_ACTIONS: dict = {}
    DETAIL_ACTIONS = {
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }

    @property
    def _detail_route(self) -> str:
        return ''

    @property
    def _detail_view_name(self) -> str:
        return self._name


class ReadOnlyModelTreeRouter(ModelTreeRouter):
    """Tree router for readonly model."""

    LIST_ACTIONS = {
        'get': 'list',
    }
    DETAIL_ACTIONS = {
        'get': 'retrieve',
    }
