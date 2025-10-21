from django.db import models
class Translation(models.Model):
    english = models.CharField(max_length=255)
    turkmen = models.CharField(max_length=255)
    def __str__(self): return f"{self.english} ↔ {self.turkmen}"
