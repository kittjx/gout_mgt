from django.urls import path
from .views import BasicConditionView

urlpatterns = [
    path('basic/', BasicConditionView.as_view(), name='condition'),
]