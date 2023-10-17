from rest_framework import serializers
from .models import News
import html
from datetime import datetime
from backend.utils import remove_html_tags, capitalize_first_character
from backend.settings import SEARCH_PATTERN, SITE_DOMAIN, REPLACE_WITH





class NewsArticleSerializer(serializers.ModelSerializer):
# specific event page...

    body = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

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
        excerpt_list = [element.strip() for element in excerpt.split('\n')]
        excerpt = ''.join(excerpt_list)
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
        model = News
        fields = ['title', 'thumbnail', 'created_at', 'body', 'excerpt']
        read_only_fields = fields




class NewsSerialezer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()


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


    def get_excerpt(self, obj):
        language = self.context.get('lang')
        excerpt = ''

        if language == 'en':
            excerpt = html.unescape(obj.english_body)
        else:
            excerpt = html.unescape(obj.greek_body)
        
        # excerpt_list = [element.strip() for element in excerpt.split('\n')]
        # excerpt = ''.join(excerpt_list)
        return capitalize_first_character(remove_html_tags(excerpt)[:500])



    def get_thumbnail(self, obj):
         return self.context['request'].build_absolute_uri(obj.thumbnail.url) 


    class Meta:
        model = News
        fields = ['title', 'excerpt', 'slug','thumbnail','created_at']