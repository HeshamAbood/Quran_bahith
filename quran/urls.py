from django.conf.urls import url
from . import views

app_name = 'quran'

urlpatterns = [
    url(r'^$', views.SoratView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^verse/$', views.VerseView.as_view(), name='verse'),
    url(r'^words/$', views.VerseWordsView.as_view(), name='words'),
    url(r'^search/$', views.QuranSearcheView.as_view(), name='search'),

    url(r'^ajax/load-verses/', views.QuranSearcheView.load_verses, name='ajax_load_verses'),  # <-- this one here

]
