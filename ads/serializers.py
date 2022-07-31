from rest_framework import serializers
from ads.models import Ad, Category, Selection


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name")

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'
