import uuid
from djongo import models


class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    launch_year = models.PositiveIntegerField()
    engine_config = models.JSONField()
    features = models.JSONField(default=list)
    colors = models.JSONField(default=list)
    categories = models.JSONField(default=list)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.manufacturer} {self.model}"
