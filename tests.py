from models import Category
from rest_framework import status
from rest_framework.test import APITestCase


class CategoryTests(APITestCase):

    def test_create_new_tree(self):
        data = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": "Category 1.1.1.1"
                                },
                                {
                                    "name": "Category 1.1.1.2"
                                },
                                {
                                    "name": "Category 1.1.1.3"
                                }
                            ]
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },
                                {
                                    "name": "Category 1.1.2.2"
                                },
                                {
                                    "name": "Category 1.1.2.3"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {
                            "name": "Category 1.2.1"
                        },
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {
                                    "name": "Category 1.2.2.1"
                                },
                                {
                                    "name": "Category 1.2.2.2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post('api/admin/categories', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 15)

    def test_retrieve_certain_category(self):
        response = self.client.get('api/admin/categories/15', format='json')
        self.assertEqual(
            response.data, {
                "id": 15,
                "name": "Category 1.1",
                "parents": [
                    {
                        "id": 11,
                        "name": "Category 1"
                    }
                ],
                "children": [
                    {
                        "id": 21,
                        "name": "Category 1.1.2.2"
                    },
                    {
                        "id": 19,
                        "name": "Category 1.1.2.1"
                    },
                    {
                        "id": 2,
                        "name": "Category 1.1.2.3"
                    },
                    {
                        "id": 27,
                        "name": "Category 1.1.2"
                    },
                    {
                        "id": 43,
                        "name": "Category 1.1.1.3"
                    },
                    {
                        "id": 32,
                        "name": "Category 1.1.1.2"
                    },
                    {
                        "id": 31,
                        "name": "Category 1.1.1.1"
                    },
                    {
                        "id": 4,
                        "name": "Category 1.1.1"
                    }
                ],
                "siblings": [
                    {
                        "id": 44,
                        "name": "Category 1.2"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
