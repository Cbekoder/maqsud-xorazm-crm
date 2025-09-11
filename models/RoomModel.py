from django.db import models


class Room(models.Model):
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

        app_label = 'common'

