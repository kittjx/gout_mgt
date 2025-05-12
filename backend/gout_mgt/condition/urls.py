from django.urls import path
from .views import BasicConditionView, PatientConditionViewSet, AdminPatientConditionViewSet

urlpatterns = [
    path('', BasicConditionView.as_view(), name='basic_condition'),
    path('view/', PatientConditionViewSet.as_view(), name='patient_condition_view'),
    path('view/all/', AdminPatientConditionViewSet.as_view(), name='all_patient_conditions'),
]
