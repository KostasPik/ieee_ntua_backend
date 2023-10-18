from rest_framework import serializers
from .models import Person





class PeopleSerializer(serializers.ModelSerializer):


    profile_pic = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        language = self.context.get('language')
        if language == 'en':
            return obj.full_name_english
        else:
            return obj.full_name_greek
        

    def get_profile_pic(self, obj):
        # request = self.context.get('request')
        # print(obj.profile_pic)
        return self.context['request'].build_absolute_uri(obj.profile_pic.url)

    class Meta:
        model = Person
        fields = ['full_name', 'role', 'profile_pic', 'society', 'facebook', 'instagram', 'email', 'linkedin']
