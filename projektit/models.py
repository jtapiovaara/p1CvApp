from django.db import models


class Projekti(models.Model):
    title = models.CharField(max_length=32, blank=True)
    shortdescription = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title

