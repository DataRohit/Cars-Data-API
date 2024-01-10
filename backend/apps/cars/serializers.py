from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    engine_config = serializers.DictField()
    features = serializers.ListField()
    colors = serializers.ListField()
    categories = serializers.ListField()

    class Meta:
        model = Car
        fields = [
            "id",
            "manufacturer",
            "model",
            "launch_year",
            "engine_config",
            "features",
            "colors",
            "categories",
            "starting_price",
        ]
