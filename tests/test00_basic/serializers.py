from rest_framework.serializers import ModelSerializer

from .models import A, B


class ASerializer(ModelSerializer):
    class Meta:
        model = A
        fields = ('id', 'x',)


class BSerializer(ModelSerializer):
    class Meta:
        model = B
        fields = ('id', 'a',)
