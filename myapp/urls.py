from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('devices/', views.devices, name='devices'),
    path('pingTest/', views.pingTest, name='pingTest'),
    path('logout/', views.signout, name='logout'),
    path('device/create/', views.deviceCreate, name='deviceCreate'),
    path('device/<int:device_id>/', views.deviceDetail, name='deviceDetail'),
    path('device/<int:device_id>/delete',
         views.deviceDelete, name='deviceDelete'),
    path('device/<int:device_id>/ping/',
         views.devicePing, name='devicePing'),
    path('signin/', views.signin, name='signin'),
]
