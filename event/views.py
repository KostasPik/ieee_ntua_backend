from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer, EventsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime
# Create your views here.

PER_PAGE = 7

@api_view(['GET'])
def get_events(request):
    language = request.query_params.get('lang', 'en')
    page = int(request.query_params.get('page', 1))
    search_param = request.query_params.get('search', None)
    order_by = int(request.query_params.get('o', 1)) #o = 1 : ascending, #o = 2: descending #o = 3: ending sooner


    # params validation here....


    if language == 'en':
        if order_by == 1:
            events = Event.objects.filter(english_version=True).prefetch_related('societies').order_by('-event_time')
        if order_by == 2:
            events = Event.objects.filter(english_version=True).prefetch_related('societies').order_by('event_time')
        if order_by == 3:
            events = Event.objects.filter(english_version=True, event_time__gte=datetime.now()).prefetch_related('societies').order_by('event_time')
    else:
        if order_by == 1:
            events = Event.objects.prefetch_related('societies').order_by('-event_time')
        if order_by == 2:
            events = Event.objects.prefetch_related('societies').order_by('event_time')
        if order_by == 3:
            events = Event.objects.filter(event_time__gte=datetime.now()).prefetch_related('societies').order_by('event_time')

    if search_param and len(search_param) > 1:
        if language == 'en':
            events = events.filter(english_title__icontains = search_param)
        else:
            events = events.filter(greek_title__icontains = search_param)

    
    paginator = Paginator(events, per_page=PER_PAGE)

    try:
        paged_announcements = paginator.get_page(int(page))
    except PageNotAnInteger:
        paged_announcements = paginator.page(1)
    except EmptyPage:
        paged_announcements = []

    events_json = EventsSerializer(paged_announcements, many=True, context={'request':request, 'lang': language})
    total_events = events.count()
    if total_events % PER_PAGE != 0:
        total_pages = int(total_events/PER_PAGE) +1
    else:
        total_pages = int(total_events/PER_PAGE)
    return Response({
        'err':False,
        'data':events_json.data,
        'total_pages': total_pages,
    })




@api_view(['GET'])
def get_event(request, event_slug):
    language = request.query_params.get('lang', 'en')
    print(language, event_slug)

    if language == 'en':
        event = Event.objects.filter(english_version=True, english_slug=event_slug)
    else:
        event = Event.objects.filter(greek_slug=event_slug)
    
    if not event.exists():
        return Response({
             'err':True,
             'found': False,
         })

    event = event.first()
    event_json = EventSerializer(event, many=False, context={"request":request, "lang":language})
    
    return Response({
        'err':False,
        'data':event_json.data
    })

import json
from datetime import datetime
from society.models import Society
@api_view(['GET'])
def load_events(request):
    json_file = 'Archive/events.json'
    with open(json_file, encoding="utf8") as f:
        json_list = json.load(f)
        print(json_list)
        for json_object in json_list:
            new_event = Event.objects.create(
                english_version=True,
                greek_title=json_object['greek_title'],
                english_title=json_object['english_title'],
                thumbnail='Archive/img/'+json_object['thumbnail'],
                greek_body=json_object['greek_body'],
                english_body=json_object['english_body'],
                event_time=json_object['event_time'],
                created_at=datetime.now())
            # chapters=[]
            for chapter in json_object['societies']:
                chapter = Society.objects.filter(short_title=chapter)
                # chapters.append(chapter)
                new_event.societies.add(chapter)
            new_event.save()
            print("Event ", json_object['english_title'], " saved")

    return Response({
        'msg':'Success',
        'data': json_list
    })