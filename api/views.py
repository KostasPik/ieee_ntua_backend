from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from event.models import Event
from datetime import datetime
# Create your views here.


@api_view(['POST'])
def contact(request):

    first_name = request.POST.get('first_name', None).strip().title()
    last_name = request.POST.get('last_name', None).strip().title()
    email = request.POST.get('email', None).strip().lower()
    subject = request.POST.get('subject', None).strip().capitalize()
    message = request.POST.get('message', None).strip()
    honeypot = request.POST.get('honeypot', False)


    if honeypot and honeypot=='true':
        return Response({
            'err': True,
            'msg': 'Bot Detected'
        })
    
    # subject and message fields are required...
    if not subject or not message or subject.strip() == '' or message.strip() == '':
        return Response({
            'err':True,
            'data': {'msg': 'Make sure all required fields are non-empty.'}
            })

    # email login here


    return_data = {
        'err': False,
    }
    return Response(return_data)


# @api_view(['POST'])
# def email_reminder(request):
    
#     email = request.POST.get('email', None).strip().lower()
#     event_slug = request.POST.get('event_slug', None).strip()
#     lang = request.POST.get('lang', None).strip()
#     print(email)

#     # event validation
#     if not event_slug or event_slug == '':
#         return Response({
#             'err': True,
#             'data': {'msg': 'No such event.'}
#             })

#     # email validation
#     if not email or email == '':
#         return Response({
#             'err': True,
#             'data': {'msg': 'Email missing'}
#             })


#     try:
#         validate_email(email)
#     except ValidationError as e:
#         return Response({
#             'err': True,
#             'data': {'msg': 'Invalid email address'}
#             })

#     # lang validation
#     if not lang or lang == '':
#         return Response({
#             'err': True,
#             'data': {'msg': 'Language not specified.'}
#             })


#     if lang == 'gr':
#         event = Event.objects.filter(greek_slug=event_slug)
#     else:
#         event = Event.objects.filter(english_slug=event_slug)


#     if not event.exists():
#         return Response({
#             'err': True,
#             'data': {'msg': 'No such event.'}
#             })

#     event = event.first()

#     if datetime.now().astimezone() > event.event_time.astimezone():
#         return Response({
#             'err': True,
#             'data': {'msg': "Event has expired... can't set reminder"}
#             })

#     # here set reminder....


#     return Response({
#         'err': False,
#         'data': {'msg': 'All good!'}
#         })


