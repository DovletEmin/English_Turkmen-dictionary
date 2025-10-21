from django.urls import path
from . import views

urlpatterns = [
    path('', views.translator_view, name='translator'),
    path('suggest/', views.suggest_words, name='suggest_words'),  # 👈 new line
]
