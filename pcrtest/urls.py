from django.urls import path

from . import views

urlpatterns = [
    path('', views.dna_input, name='dna_input'),
    path('dna-input/', views.dna_input, name='dna-input'),
    path('forward-primer/', views.forward_primer, name='forward-primer'),
    path('reverse-primer/', views.reverse_primer, name='reverse-primer'),
    path('clear-session/', views.clear_session, name='clear-session')
]
