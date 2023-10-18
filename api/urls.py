from django.urls import path
from event.views import get_events, get_event, load_events
from society.views import get_society
from .views import contact
from news.views import get_news, get_news_article
from awards.views import get_awards
from people.views import get_board

urlpatterns = [
    path('events/', get_events, name='events'),
    path('event/<str:event_slug>',get_event, name='event'),
    path('society/<str:society_slug>', get_society, name='society'),
    path('contact/', contact, name='contact'),
    # path('email-reminder/',email_reminder, name='email-reminder'),
    path('news/',get_news, name='news'),
    path('news/article/<str:news_slug>/', get_news_article, name='get-news-article'),
    # path('load-events/',load_events),
    path('awards/', get_awards),
    path('board', get_board),
]
