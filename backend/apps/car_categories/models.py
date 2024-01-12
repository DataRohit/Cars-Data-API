import uuid
from djongo import models


class CarCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255, unique=True)
    baseline_parameters = models.JSONField()
    description = models.TextField()

    def __str__(self):
        return str(self.category_name)
