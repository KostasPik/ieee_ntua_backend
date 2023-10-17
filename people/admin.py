from django.contrib import admin
from .models import Person
# Register your models here.



class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name_greek', 'full_name_english','society', 'role',]

    fields = ['full_name_greek', 'full_name_english','role', 'society', 'profile_pic', 'facebook', 'instagram', 'email', 'linkedin']
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('full_name_english','society',)
        return self.readonly_fields


admin.site.register(Person, PersonAdmin)