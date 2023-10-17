from django.contrib import admin
from .models import Society, SubGroup


# Register your models here.





class SocietyAdmin(admin.ModelAdmin):
    # prepopulated_fields = {
    #     'slug': ('title',)
    # }
    list_display = ['title', 'short_title',]

    fields = ['title','short_title','logo','hero_image','greek_body', 'english_body', 'recruitment_form','subgroup_label',
              'page_color', 'facebook', 'instagram', 'tiktok', 'email']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('title',)
        return self.readonly_fields

class SubgroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'society',]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('title','society')
        return self.readonly_fields


admin.site.register(SubGroup, SubgroupAdmin)
admin.site.register(Society, SocietyAdmin)