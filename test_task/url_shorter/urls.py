from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.shortened_links, name='shotenedlinks'),
    path('<subpart>/', views.redirect_by_short_link, name='redirect'),
]