from rest_framework import serializers
from .models import CarCategory


class CarCategorySerializer(serializers.ModelSerializer):
    baseline_parameters = serializers.DictField()

    class Meta:
        model = CarCategory
        fields = ["id", "category_name", "baseline_parameters", "description"]
