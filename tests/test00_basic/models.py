from django.db import models


class A(models.Model):
    x = models.IntegerField()


class B(models.Model):
    a = models.ForeignKey(
        A, on_delete=models.CASCADE,
    )
