from django.urls import path
from .views import MyView

urlpatterns = [
    path('my-view/', MyView.as_view()),

]
