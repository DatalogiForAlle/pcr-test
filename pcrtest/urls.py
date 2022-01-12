from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('forward-primer/', views.forward_primer, name='forward-primer'),
    path('reverse-primer/', views.reverse_primer, name='reverse-primer')
]
