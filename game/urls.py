from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('rsp/', views.rsp_select, name='rsp_select'),
    path('rsp/<str:pick>', views.rsp_result, name='rsp_result'),
    path('rsp/reset/', views.rsp_reset, name='rsp_reset'),
    path('weapon/create/', views.weapon_create, name='weapon_create'),
    path('weapon/list/', views.weapon_list, name='weapon_list'),
    path('adventure/home/', views.adventure_home, name='adventure_home'),
    path('weapon/get/', views.weapon_get, name='weapon_get'),
]
