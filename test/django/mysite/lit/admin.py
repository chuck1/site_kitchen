from django.contrib import admin

# Register your models here.

from lit.models import Publication
from lit.models import Author
from lit.models import Tag

#admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Tag)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('code','title')

admin.site.register(Publication, PublicationAdmin)

