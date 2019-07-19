from django.urls import include, path

from drf_tree_routers.base import RootRouter
from drf_tree_routers.model import ModelTreeRouter

from .views import AViewSet, BViewSet

router = RootRouter()
a = router['a/'] = ModelTreeRouter(
    viewset=AViewSet,
    name='a',
)
a['b/'] = ModelTreeRouter(
    viewset=BViewSet,
    name='b',
)

urlpatterns = [
    path('', include(router.urls)),
]
