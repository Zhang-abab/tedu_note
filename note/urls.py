from . import views
from django.urls import path

urlpatterns = [
    path('add',views.add_note),
    path('list/<int:uid>',views.list_note),
]