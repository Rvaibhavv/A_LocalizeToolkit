from django.urls import path
from . import views

app_name ='descriptionprovider'

urlpatterns = [
    path('',views.index,name='desP_Home')
]