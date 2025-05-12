from django.urls import path
from .views import RecordView

urlpatterns = [
    path('', RecordView.as_view(), name='records'),
    path('<int:record_id>/', RecordView.as_view(), name='record_detail'),
]
