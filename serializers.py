from rest_framework import serializers
from random import randrange

from models import Category


__all__ = [
    'CategoriesSaveSerializer', 'CategoryExtendedSerializer'
]


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class CategoryExtendedSerializer(CategorySerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    siblings = serializers.SerializerMethodField()

    def get_parents(self, obj):
        return CategorySerializer(
            obj['parents'], many=True
        ).data

    def get_children(self, obj):
        return CategorySerializer(
            obj['children'], many=True
        ).data

    def get_siblings(self, obj):
        return CategorySerializer(
            obj['siblings'], many=True
        ).data


class CategoriesSaveSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    ALREADY_USED_IDS = set()

    def validate(self, data):
        data = super(CategoriesSaveSerializer, self).validate(data)
        if 'children' in self.initial_data:
            objs = []
            for cat in self.initial_data['children']:
                serializer = self.__class__(
                    data=cat
                )
                serializer.is_valid()
                objs.append(serializer.validated_data)
            data['children'] = objs
        return data

    @classmethod
    def generate_id(cls):
        id = randrange(1, 50)
        while id in cls.ALREADY_USED_IDS:
            id = randrange(1, 50)
        cls.ALREADY_USED_IDS.add(id)
        return id

    @classmethod
    def create_obj(cls, categories, parent_id):
        objs_to_create = []
        for cat in categories:
            head_id = cls.generate_id()
            objs_to_create.append(
                Category(
                    id=head_id,
                    name=cat['name'],
                    parent_id=parent_id
                )
            )
            children = cat.get('children')
            if children:
                objs_to_create += cls.create_obj(children, head_id)
        return objs_to_create

    def create(self, validated_data):
        head_id = self.generate_id()
        to_create_cats = [
            Category(
                name=validated_data['name'],
                id=head_id
            )
        ]
        to_create_cats += self.create_obj(validated_data['children'], head_id)
        return Category.objects.bulk_create(to_create_cats)
