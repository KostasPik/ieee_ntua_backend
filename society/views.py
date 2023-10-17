from django.shortcuts import render
from .models import Society, SubGroup
from .serializers import SocietySerializer, SubGroupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


import html
@api_view(['GET'])
def get_society(request, society_slug):
    language = request.query_params.get('lang', 'en')
    society = Society.objects.filter(slug=society_slug)
    if not society.exists():
        return Response({
            'err': True,
            'found': False,
        })
    
    society = society.first()

    # subgroups = society.subgroup_set.all()
    society_json = SocietySerializer(society, many=False, context={'lang':language, 'request':request})
    # subgroups_json = SubGroupSerializer(subgroups, many=True, context={'lang':language, 'request':request})
    

    return Response({
        'err': False,
        'data': society_json.data
    })
