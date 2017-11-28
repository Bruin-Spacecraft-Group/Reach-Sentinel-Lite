from django.conf.urls import url

from . import views

app_name = 'graphs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getdata/(?P<sensor>[0-9])/$', views.getdata, name='getdata'),
    url(r'^getdata/$', views.getdata, name='getdata')
]