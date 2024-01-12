from rest_framework import serializers
from .models import CarPart


class CarPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPart
        fields = [
            "id",
            "part_name",
            "part_number",
            "description",
            "manufacturer",
            "price",
        ]
