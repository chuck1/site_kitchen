from django.db import models

# Create your models here.

class Location(models.Model):
    name     = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Area(models.Model):
    name     = models.CharField(max_length=256)
    
    location = models.ForeignKey(Location, null=True)
    def __unicode__(self):
        return self.name

class Wall(models.Model):
    name     = models.CharField(max_length=256)
    
    location = models.ForeignKey(Location, null=True, blank=True)
    area     = models.ForeignKey(Area, null=True, blank=True)
    def __unicode__(self):
        return self.name

class Route(models.Model):
    name     = models.CharField(max_length=256)
    
    location = models.ForeignKey(Location, null=True)
    area     = models.ForeignKey(Area, null=True)
    wall     = models.ForeignKey(Wall, null=True)
    
    def __unicode__(self):
        return self.name

class Pitch(models.Model):
    name     = models.CharField(max_length=256)

    route = models.ForeignKey(Route)

    def __unicode__(self):
        return self.name

