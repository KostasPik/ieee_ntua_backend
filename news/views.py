from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import News
from rest_framework.response import Response
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .serializers import NewsSerialezer, NewsArticleSerializer



PER_PAGE = 3

# Create your views here.
@api_view(['GET'])
def get_news(request):
    language = request.query_params.get('lang', 'en')
    page = int(request.query_params.get('page', 1))
    search_param = request.query_params.get('search', None)
    order_by = int(request.query_params.get('o', 1)) #o = 1 : ascending, #o = 2: descending #o = 3: ending sooner


    # params validation here....


    if language == 'en':
        if order_by == 1:
            news = News.objects.filter(english_version=True).order_by('-created_at')
        if order_by == 2:
            news = News.objects.filter(english_version=True).order_by('created_at')
    else:
        if order_by == 1:
            news = News.objects.order_by('-created_at')
        if order_by == 2:
            news = News.objects.order_by('created_at')
    
    if search_param and len(search_param) > 1:
        if language == 'en':
            news = news.filter(english_title__icontains = search_param)
        else:
            news = news.filter(greek_title__icontains = search_param)

    
    paginator = Paginator(news, per_page=PER_PAGE)

    try:
        paged_announcements = paginator.get_page(int(page))
    except PageNotAnInteger:
        paged_announcements = paginator.page(1)
    except EmptyPage:
        paged_announcements = []

    news_json = NewsSerialezer(paged_announcements, many=True, context={'request':request, 'lang': language})
    total_news = news.count()
    if total_news % PER_PAGE != 0:
        total_pages = int(total_news/PER_PAGE) + 1
    else:
        total_pages = int(total_news/PER_PAGE)
    return Response({
        'err':False,
        'data':news_json.data,
        'total_pages': total_pages,
    })



@api_view(['GET'])
def get_news_article(request, news_slug):
    language = request.query_params.get('lang', 'en')

    if language == 'en':
        news_article = News.objects.filter(english_version=True, english_slug=news_slug)
    else:
        news_article = News.objects.filter(greek_slug=news_slug)
    
    if not news_article.exists():
        return Response({
             'err':True,
             'found': False,
         })

    news_article = news_article.first()
    news_article_json = NewsArticleSerializer(news_article, many=False, context={"request":request, "lang":language})
    
    return Response({
        'err':False,
        'data':news_article_json.data
    })