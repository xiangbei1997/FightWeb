from django.urls import path, re_path
from Analysis import views


urlpatterns = [
    path('Capital.html', views.CapitalExhibition),
    path('CapitalData', views.CapitalData),
    path('Seniority', views.Seniority),
    path('Record.html', views.RecordPage),
    path('Record2.html', views.Record2),
    path('RecordData', views.RecordData),
    path('Search.html', views.Search),
    path('vagueSearch', views.vagueSearch),
]
