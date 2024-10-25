from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('success/', views.review_success, name='review_success'),
]
