from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from emissary.main import views

urlpatterns = [
    path('', views.LinkList.as_view()),
    path('<slug:slug>/', views.Landing.as_view()),
]
