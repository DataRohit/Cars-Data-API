import json
from django.conf import settings
from django.core.management.base import BaseCommand
from backend.apps.car_parts.models import CarPart


class Command(BaseCommand):
    help = "Load car parts data from a JSON file into the database"

    def handle(self, *args, **options):
        json_file_path = settings.BASE_DIR / "data" / "car_parts.json"

        with open(json_file_path, "r") as file:
            car_parts_data = json.load(file)

        for car_part_data in car_parts_data:
            car_part_instance = CarPart.objects.create(
                part_name=car_part_data["part_name"],
                part_number=car_part_data["part_number"],
                description=car_part_data["description"],
                manufacturer=car_part_data["manufacturer"],
                price=car_part_data["price"],
            )
            car_part_instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded car parts data"))
