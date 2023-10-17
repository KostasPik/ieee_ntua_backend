from django.contrib import admin
from .models import Event


# Register your models here.


class EventAdmin(admin.ModelAdmin):
    # prepopulated_fields = {
    #     'greek_slug': ('greek_title', ),
    #     'english_slug': ('english_title', )

    # }
    list_display = ['greek_title', 'event_time','has_english_version']

    fields = ['english_version', 'greek_title', 'english_title',
            'thumbnail', 'societies',
              'greek_body', 'english_body','event_time', 'greek_event_place', 'english_event_place']
    
    def has_english_version(self, obj):
        return obj.english_version
    has_english_version.boolean=True

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('greek_title',)
        return self.readonly_fields

admin.site.register(Event, EventAdmin)