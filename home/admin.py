from django.contrib import admin
from .models import University, Field, Group

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')

admin.site.register(University)
admin.site.register(Field)
admin.site.register(Group, GroupAdmin)