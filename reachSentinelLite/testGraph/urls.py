from django.conf.urls import url

from . import views

app_name = 'testGraph'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testing/$', views.testing, name='testing'),
    url(r'^getdata/$', views.getdata, name='getdata')
]