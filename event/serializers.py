from rest_framework import serializers
from .models import Event
from society.models import Society
import html
from datetime import datetime
from backend.utils import remove_html_tags, capitalize_first_character
from backend.settings import SITE_DOMAIN, REPLACE_WITH, SEARCH_PATTERN



class EventsSocietySerializer(serializers.ModelSerializer): # used for serializing society field in Events pagfe
    class Meta:
        model = Society
        fields = ['slug', 'short_title', 'page_color']
        read_only_fields = fields

class EventsSerializer(serializers.ModelSerializer):
# events that are shown in events page...
    expired = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    mobile_thumbnail = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()

    societies = EventsSocietySerializer(many=True, read_only=True)


    def get_place(self, obj):
        language = self.context.get('lang')

        if language == 'en':
            place = obj.english_event_place
        else:
            place = obj.greek_event_place

        return place

    def get_title(self, obj):
        language = self.context.get('lang')

        if language == 'en':
            title = obj.english_title
        else:
            title = obj.greek_title

        return title

    def get_slug(self, obj):
        language = self.context.get('lang')

        if language == 'en':
            slug = obj.english_slug
        else:
            slug = obj.greek_slug
        return slug
    
    def get_expired(self, obj):
        if datetime.now().astimezone() > obj.event_time.astimezone():
            return True
        return False

    def get_excerpt(self, obj):
        language = self.context.get('lang')
        excerpt = ''

        if language == 'en':
            excerpt = html.unescape(obj.english_body)
        else:
            excerpt = html.unescape(obj.greek_body)
        return capitalize_first_character(remove_html_tags(excerpt)[:500])


    def get_mobile_thumbnail(self, obj):
         return self.context['request'].build_absolute_uri(obj.mobile_thumbnail.url) 

    def get_thumbnail(self, obj):
         return self.context['request'].build_absolute_uri(obj.thumbnail.url) 
    

    class Meta:
        model = Event
        fields = ['title', 'slug','thumbnail', 'mobile_thumbnail', 'societies', 'expired', 'event_time', 'excerpt', 'place']
        read_only_fields = fields


class EventSerializer(serializers.ModelSerializer):
# specific event page...

    body = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    societies = EventsSocietySerializer(many=True, read_only=True)
    place = serializers.SerializerMethodField()
    
    
    def get_place(self, obj):
        language = self.context.get('lang')

        if language == 'en':
            place = obj.english_event_place
        else:
            place = obj.greek_event_place

        return place
    def get_title(self, obj):
        language = self.context.get('lang')

        if language == 'en':
            title = obj.english_title
        else:
            title = obj.greek_title

        return title


    def get_excerpt(self, obj):
        language = self.context.get('lang')
        excerpt = ''

        if language == 'en':
            excerpt = html.unescape(obj.english_body)
        else:
            excerpt = html.unescape(obj.greek_body)
        excerpt = ''.join([element.strip() for element in excerpt.split('\n')])
        return capitalize_first_character(remove_html_tags(excerpt)[:500])



    def get_body(self, obj): # choose if we are going to send greek or english body...
        language = self.context.get('lang')

        if language == 'en':
            body = html.unescape(obj.english_body)
        else:
            body = html.unescape(obj.greek_body)
        
        # Fixes django ckeditor relative paths for images...
        body = body.replace(SEARCH_PATTERN, REPLACE_WITH)

        return body
    
    class Meta:
        model = Event
        fields = ['title', 'thumbnail', 'mobile_thumbnail', 'event_time', 'body', 'excerpt', 'societies', 'place']
        read_only_fields = fields