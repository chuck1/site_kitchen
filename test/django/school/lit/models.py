from django.db import models

# Create your models here.

class Author(models.Model):
    name1 = models.CharField(max_length=128)
    name2 = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name1 + ", " + self.name2

class Tag(models.Model):
    name = models.CharField(max_length=64)

class Publication(models.Model):
    title = models.CharField(max_length=512)
    bib = models.TextField()
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag)




