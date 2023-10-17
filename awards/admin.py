from django.contrib import admin
from .models import Award
# Register your models here.





class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'society']


admin.site.register(Award, AwardAdmin)
