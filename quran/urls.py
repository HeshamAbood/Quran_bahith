from django.conf.urls import url
from . import views

app_name = 'quran'

urlpatterns = [
    url(r'^$', views.SoratView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^verse/$', views.VerseView.as_view(), name='verse'),
    url(r'^words/$', views.VerseWordsView.as_view(), name='words'),
    url(r'^search/$', views.QuranSearcheView.as_view(), name='search'),
    url(r'^search/$', views.QuranSearcheExport.as_view(), name='search_csv'),

    url(r'^ajax/load-verses/', views.QuranSearcheView.load_verses, name='ajax_load_verses'),  # <-- this one here
    url(r'^ajax/load-search-result/', views.QuranSearcheView.load_search_result, name='ajax_load_search_result'),  # <-- this one here

]
