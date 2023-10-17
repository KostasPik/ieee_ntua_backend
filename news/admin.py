from django.contrib import admin
from .models import News
# Register your models here.



class NewsAdmin(admin.ModelAdmin):
    list_display = ['greek_title', 'created_at','has_english_version']

    fields = ['english_version', 'greek_title', 'english_title',
              'thumbnail',
              'greek_body', 'english_body']
    
    
    def has_english_version(self, obj):
        return obj.english_version
    has_english_version.boolean = True


    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('greek_title',)
        return self.readonly_fields

admin.site.register(News, NewsAdmin)