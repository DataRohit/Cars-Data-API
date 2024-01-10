import json
from django.conf import settings
from django.core.management.base import BaseCommand
from backend.apps.cars.models import Car


class Command(BaseCommand):
    help = "Load car data from a JSON file into the database"

    def handle(self, *args, **options):
        json_file_path = settings.BASE_DIR / "data" / "cars.json"

        with open(json_file_path, "r") as file:
            cars_data = json.load(file)

        for car_data in cars_data:
            car_instance = Car.objects.create(
                manufacturer=car_data["manufacturer"],
                model=car_data["model"],
                launch_year=car_data["launch_year"],
                engine_config=car_data["engine_config"],
                features=car_data["features"],
                colors=car_data["colors"],
                categories=car_data["categories"],
                starting_price=car_data["starting_price"],
            )
            car_instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully loaded car data"))
