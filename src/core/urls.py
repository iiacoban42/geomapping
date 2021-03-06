"""Core urls module"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

# pylint: disable=all

urlpatterns = [
    path('captcha/', views.captcha, name='captcha'),
    path('captcha_embed/', views.captcha_embed, name='captcha_embed'),
    path('get_tile/', views.get_tile, name='get_tile'),
    path('submit_captcha/', csrf_exempt(views.submit_captcha), name='submit_captcha'),
    path('tiles_overview/', views.tiles_overview, name='tiles_overview'),
    path('embed_example/', views.embed_example, name='embed_example'),
    path('get_labels/<tile>/', views.get_labels, name='get_labels'),
    path('get_all_labels/<requested_map>/', views.get_all_labels, name='get_all_labels'),
    path('get_statistics/', views.get_statistics, name='get_statistics'),
    path('get_markers/', views.get_markers, name='get_markers'),
    path('get_statistics_year/<requested_year>/', views.get_statistics_year, name='get_statistics_year'),
    path('get_accuracy/', views.get_accuracy, name='get_accuracy'),
    path('machine_learning/', views.machine_learning, name='machine_learning'),
    path('train/', views.train, name='train'),
    path('', views.home, name='index')
]
