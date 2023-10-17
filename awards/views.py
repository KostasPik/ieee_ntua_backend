from django.shortcuts import render
from .models import Award
from .serializers import AwardsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.



@api_view(['GET'])
def get_awards(request):
    
    awards = Award.objects.all().order_by("-year")
    awards_json = AwardsSerializer(awards, many=True)
    

    new_json = {}
    # make json grouped by society
    for award in awards_json.data:
        society = award['society']
        if society == None:
            society = 'IEEE NTUA SB'
        
        new_json[society] = []

    for award in awards_json.data:
        society = award['society']
        if society == None:
            society = 'IEEE NTUA SB'

        
        new_json[society].append(award)
    print(new_json)
    return Response({
        'err': False,
        'data': new_json
    })