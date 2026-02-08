
from django.urls import path

from Users import views

urlpatterns = [
    path('list-view/',views.ListView.as_view(),name='listview'),
    path('',views.MainView,name='mainview'),
    path('organization/<int:pk>',views.DetailView,name='detailview'),
]
