from django.urls import path
from .views import get_reviews, enter_url

urlpatterns = [
    path('api/reviews/', get_reviews, name='get_reviews'),
    path('enter-url/', enter_url, name='enter_url'),
]
