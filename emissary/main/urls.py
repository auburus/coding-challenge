from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from emissary.main import views

urlpatterns = [
    path('', views.LinkList.as_view(), name='link-list'),
    path('<int:pk>/', views.LinkDetails.as_view(), name='link-details'),
    path('<slug:slug>/', views.Landing.as_view(), name='landing'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
