from django.shortcuts import render
from .models import Person
from .serializers import PeopleSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def get_board(request):
    board = Person.objects.filter(society__isnull=True).all()
    board_serializer = PeopleSerializer(board, many=True, read_only=True)
    return Response({
        "error": False,
        "data": board_serializer.data
    })