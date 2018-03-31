from django.conf.urls import url
from . import views
app_name = 'comments'
urlpatterns = [
    url(r'^comments/article/(?P<article_pk>[0-9]+)/$', views.article_comment, name='article_comment'),
]