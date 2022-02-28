from . import views
from django.urls import path

urlpatterns = [
    path('reg',views.reg_view),
    path('login',views.login_view),
    path('logout', views.logout_view),
    
]