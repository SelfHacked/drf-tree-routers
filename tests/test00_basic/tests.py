from django.test import TestCase
from rest_framework.test import APIClient


class TestRoot(TestCase):
    fixtures = ['fixtures']

    def setUp(self) -> None:
        self.client = APIClient()

    def test_root(self):
        response = self.client.get(
            '/',
            format='json',
        )
        assert response.status_code == 200
        assert list(response.data) == [
            [
                "/a/",
                [
                    "/a/<a_id>/",
                    [
                        "/a/<a_id>/b/",
                        "/a/<a_id>/b/<b_id>/",
                    ],
                ],
            ],
        ]


class TestModel(TestCase):
    fixtures = ['fixtures']

    def setUp(self) -> None:
        self.client = APIClient()

    def test_a_list(self):
        response = self.client.get(
            '/a/',
            format='json',
        )
        assert response.status_code == 200
        assert list(response.data) == [
            {
                'id': 1,
                'x': 100,
            },
            {
                'id': 2,
                'x': 555,
            },
        ]

    def test_a_detail(self):
        response = self.client.get(
            '/a/1/',
            format='json',
        )
        assert response.status_code == 200
        assert dict(response.data) == {
            'id': 1,
            'x': 100,
        }

    def test_b_list(self):
        response = self.client.get(
            '/a/1/b/',
            format='json',
        )
        assert response.status_code == 200
        assert list(response.data) == [
            {
                'id': 1,
                'a': 1,
            },
            {
                'id': 3,
                'a': 1,
            },
        ]

    def test_b_detail(self):
        response = self.client.get(
            '/a/1/b/3/',
            format='json',
        )
        assert response.status_code == 200
        assert dict(response.data) == {
            'id': 3,
            'a': 1,
        }
