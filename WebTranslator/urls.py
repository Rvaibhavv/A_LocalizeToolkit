from django.urls import path
from . import views

app_name ='webtranslator'

urlpatterns = [
    path('',views.index,name='webT_Home'),
    path('language/',views.language,name='language')
]