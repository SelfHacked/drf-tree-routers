from rest_framework.viewsets import ModelViewSet

from .models import A, B
from .serializers import ASerializer, BSerializer


class AViewSet(ModelViewSet):
    queryset = A.objects.all()
    serializer_class = ASerializer
    lookup_url_kwarg = 'a_id'


class BViewSet(ModelViewSet):
    serializer_class = BSerializer
    lookup_url_kwarg = 'b_id'

    def get_queryset(self):
        return B.objects.filter(
            a_id=self.kwargs['a_id'],
        )
