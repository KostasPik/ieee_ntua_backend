from rest_framework import serializers
from .models import Society, SubGroup
from event.models import Event
from event.serializers import EventsSerializer
from people.serializers import  PeopleSerializer
from people.models import Person
import html


class SubGroupSerializer(serializers.ModelSerializer):
    
    thumbnail = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    def get_body(self, obj):
        language = self.context.get('lang')
        if language == 'en':
            return html.unescape(obj.english_body)
        else:
            return html.unescape(obj.greek_body)

    def get_thumbnail(self, obj):
        return self.context['request'].build_absolute_uri(obj.thumbnail.url)

    class Meta:
        model = SubGroup
        fields = ["thumbnail", "title", "body"]
        read_only_fields = fields



class SocietySerializer(serializers.ModelSerializer):


    body        = serializers.SerializerMethodField()
    logo        = serializers.SerializerMethodField()
    subgroups   = serializers.SerializerMethodField()
    events      = serializers.SerializerMethodField()
    people      = serializers.SerializerMethodField()


    def get_people(self, obj):
        request = self.context.get('request')
        language = self.context.get('lang')
        people = Person.objects.filter(society=obj.pk).all()
        people_json = PeopleSerializer(people, many=True, context={'request': request, 'language': language})
        return people_json.data

    def get_events(self, obj):
        language = self.context.get('lang')
        request = self.context.get('request')
        if language == 'en':
                events = Event.objects.filter(societies=obj.pk, english_version=True).all().order_by("-event_time")[:4]
        else:
                events = Event.objects.filter(societies=obj.pk).all().order_by("-event_time")[:4]
        event_json = EventsSerializer(events, many=True, context={'lang': language, 'request': request})
        return event_json.data

    def get_subgroups(self, obj):
        language = self.context.get('lang')
        request = self.context.get('request')
        subgroups = SubGroup.objects.filter(society=obj.pk).all()
        subgroups_json = SubGroupSerializer(subgroups, many=True, context={'lang':language, 'request':request})
        return subgroups_json.data

    def get_body(self, obj):
        language = self.context.get('lang')
        if language == 'en':
            return html.unescape(obj.english_body)
        else:
            return html.unescape(obj.greek_body)

    def get_hero_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.hero_image) 

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url) 

    class Meta:
        model = Society
        fields = ['title', 'short_title','logo', 'hero_image', 'body', 
                  'page_color', 'events', 'subgroups', 'subgroup_label', 
                  'people', 'facebook', 'instagram', 'linkedin', 'email', 'tiktok', "recruitment_form"]
        read_only_fields = fields