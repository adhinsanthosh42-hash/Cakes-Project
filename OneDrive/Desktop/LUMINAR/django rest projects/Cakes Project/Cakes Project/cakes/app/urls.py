from django.urls import path
from .import views

urlpatterns = [
    path('cakes/', views.CakeCreateListCreateView.as_view()),
    path('cakes/<int:id>/', views.CakeRetrieveUpdateDestroyView.as_view()),
]
