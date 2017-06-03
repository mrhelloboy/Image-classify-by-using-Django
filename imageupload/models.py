from django.db import models

class Image(models.Model):

    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.photo.name