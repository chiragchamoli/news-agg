from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Feed
from .forms import FeedForm
from django.shortcuts import redirect


import feedparser
import datetime
# Create your views here.
def articles_list(request):
	articles = Article.objects.all();
	#
	return render(request, 'news/articles_list.html',{'articles': articles})

def feeds_list(request):
	feeds = Feed.objects.all();
	return render(request, 'news/feeds_list.html',{'feeds': feeds})	

def feed_new(request):
	if request.method == "POST":
		form = FeedForm(request.POST)
		if form.is_valid():
			feed = form.save(commit=False)

			existingFeed = Feed.objects.filter(url = feed.url)
		
			feeddata = feedparser.parse(feed.url)
			feed.title = feeddata.feed.title
			feed.save()

			for entry in feeddata.entries:
				article = Article()
				article.title = entry.title
				article.url = entry.link
				article.description = entry.description
				
				d =  datetime.datetime(*(entry.published_parsed[0:6]))
				dateString = d.strftime('%Y-%m-%d %H:%M:%S')
				article.publication_date = dateString
				article.feed = feed
				article.save()

			return redirect('news.views.feeds_list')
	else:
		form = FeedForm()
		return render(request, 'news/feed_new.html',{'form': form})	
