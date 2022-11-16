from django.db import models

# Create your models here.
class Weapon(models.Model):
    name = models.CharField(max_length=20)
    power = models.IntegerField()

    def __str__(self):
        return self.name

class Character(models.Model):
    nickname = models.CharField(max_length=20)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, related_name='character_list', null=True, blank=True)

    def __str__(self):
        return self.nickname
