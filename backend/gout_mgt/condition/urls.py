from django.urls import path
from .views import BasicConditionView

urlpatterns = [
    path('', BasicConditionView.as_view(), name='condition'),
]