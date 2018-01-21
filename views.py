from django.shortcuts import get_object_or_404
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import CategoriesSaveSerializer, CategoryExtendedSerializer
from models import Category

__all__ = ['CategoriesView']


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class CategoriesView(APIView):
    RETRIEVING_QUERY = """
        WITH RECURSIVE tree(id, name, parents, level) AS (
          SELECT id, name, ARRAY[id], 1 as level
          FROM companies_category
          WHERE companies_category.parent_id is NULL
        UNION ALL
          SELECT cc.id, cc.name, parents || cc.id, tree.level + 1
          FROM tree
          JOIN companies_category as cc ON cc.parent_id=tree.id
        )
        SELECT * FROM tree order by parents DESC;
    """

    def post(self, request, category_id=None):
        serializer = CategoriesSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)

    @staticmethod
    def create_cat_obj(id, name):
        return {
            'id': id,
            'name': name
        }

    def get(self, request, category_id):
        category = get_object_or_404(
            Category,
            id=category_id
        )
        category_id = category.id
        with connection.cursor() as cursor:
            cursor.execute(self.RETRIEVING_QUERY)
            data = dictfetchall(cursor)

        needed_category = next(cat for cat in data if cat['id'] == category_id)
        parent_ids = needed_category['parents']
        parent_ids.remove(needed_category['id'])
        level = needed_category['level']
        response_data = {
            'parents': [],
            'children': [],
            'siblings': []
        }
        response_data.update(
            self.create_cat_obj(
                category.id,
                needed_category['name']
            )
        )

        for cat in data:
            # siblings
            parents_difference = set(
                cat['parents']
            ).symmetric_difference(needed_category['parents'])
            try:
                parents_difference.remove(cat['id'])
                parents_difference.remove(category_id)
            except KeyError:
                pass
            if cat['level'] == level and cat['id'] != category_id and not parents_difference:
                response_data['siblings'].append(
                    self.create_cat_obj(
                        cat['id'], cat['name']
                    )
                )
            # parents
            if cat['id'] in parent_ids:
                response_data['parents'].append(
                    self.create_cat_obj(
                        cat['id'], cat['name']
                    )
                )
            # children
            if category_id in cat['parents']:
                response_data['children'].append(
                    self.create_cat_obj(
                        cat['id'], cat['name']
                    )
                )

        return Response(
            CategoryExtendedSerializer(response_data).data
        )
