from django.urls import path
from .views import RecordView, UserRecordsViewSet

urlpatterns = [
    path('', RecordView.as_view(), name='records'),
    path('<int:record_id>/', RecordView.as_view(), name='record_detail'),
    path('view/all/', UserRecordsViewSet.as_view(), name='user_records_view'),
]
