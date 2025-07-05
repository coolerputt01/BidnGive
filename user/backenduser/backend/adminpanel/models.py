from django.db import models
from datetime import time

class MergeSettings(models.Model):
    morning_time = models.TimeField(default=time(8, 0))
    evening_time = models.TimeField(default=time(18, 30))
    auction_duration_minutes = models.IntegerField(default=3)  # New
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Merge Times: {self.morning_time}, {self.afternoon_time}, {self.evening_time}"
