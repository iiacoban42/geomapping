"""Core urls module"""
from django.urls import path
from core import views
from django.views.decorators.csrf import csrf_exempt

# pylint: disable=all

urlpatterns = [
    path('captcha/', views.captcha, name='captcha'),
    path('get_tile/', views.get_tile, name='get_tile'),
    path('submit_captcha/', csrf_exempt(views.submit_captcha), name='submit_captcha'),
    path('tiles_overview/', views.tiles_overview, name='tiles_overview'),
    path('get_statistics/', views.get_statistics, name='get_statistics'),
    path('get_statistics_year/<requested_year>/', views.get_statistics_year, name='get_statistics_year'),
    path('', views.home, name='index')
]
