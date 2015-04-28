from django.contrib import admin

# Register your models here.

import task.models

admin.site.register(task.models.Task)

