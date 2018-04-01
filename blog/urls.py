from django.conf.urls import url
from blog.feeds import AllArticleRssFeed

from blog import views
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),#将类视图转换成函数视图非常简单，只需调用类视图的 as_view() 方法即可
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)$', views.TagView.as_view(), name='tag'),
    url(r'^all/rss/$', AllArticleRssFeed(), name='rss')
]