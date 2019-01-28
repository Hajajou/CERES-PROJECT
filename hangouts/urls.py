from django.urls import include, path
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('traceforum/',views.traceforum,name='traceforum'),
]
