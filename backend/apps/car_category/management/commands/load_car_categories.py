import json
from django.conf import settings
from django.core.management.base import BaseCommand
from backend.apps.car_category.models import CarCategory


class Command(BaseCommand):
    help = "Load car categories data from a JSON file into the database"

    def handle(self, *args, **options):
        json_file_path = settings.BASE_DIR / "data" / "car_categories.json"

        with open(json_file_path, "r") as file:
            categories_data = json.load(file)

        for category_data in categories_data:
            category_instance = CarCategory.objects.create(
                category_name=category_data["category_name"],
                baseline_parameters=category_data["baseline_parameters"],
                description=category_data["description"],
            )
            category_instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded car categories data"))
