from django.urls import path, re_path
from Analysis import views


urlpatterns = [
    path('zhucezijing', views.CapitalExhibition),
    path('CapitalData', views.CapitalData),
]
