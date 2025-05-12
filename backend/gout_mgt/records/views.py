from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.auth import TokenAuthentication
from django.db import transaction
from .models import (
    Record, WeightRecord, MainFoodRecord, WaterIntakeRecord, 
    PurineFoodRecord, UricAcidRecord, UrinePHRecord, LiverFunctionRecord,
    KidneyFunctionRecord, BloodSugarRecord, BloodPressureRecord, BloodLipidRecord,
    AttackRecord, TophiRecord, SurgeryRecord, JointFunctionRecord
)
from .serializers import (
    RecordSerializer, WeightRecordSerializer, MainFoodRecordSerializer, 
    WaterIntakeRecordSerializer, PurineFoodRecordSerializer, UricAcidRecordSerializer,
    UrinePHRecordSerializer, LiverFunctionRecordSerializer,
    KidneyFunctionRecordSerializer, BloodSugarRecordSerializer, BloodPressureRecordSerializer,
    BloodLipidRecordSerializer, AttackRecordSerializer, TophiRecordSerializer,
    SurgeryRecordSerializer, JointFunctionRecordSerializer
)
import logging
import json


logger = logging.getLogger(__name__)

class RecordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get all records for the user
            records = Record.objects.filter(user=request.user)
            
            # Group by record_type
            grouped_records = {}
            
            # Define record type configurations
            record_types = {
                'weight': {
                    'model': WeightRecord,
                    'serializer': WeightRecordSerializer,
                },
                'mainFood': {
                    'model': MainFoodRecord,
                    'serializer': MainFoodRecordSerializer,
                },
                'waterIntake': {
                    'model': WaterIntakeRecord,
                    'serializer': WaterIntakeRecordSerializer,
                },
                'purineFood': {
                    'model': PurineFoodRecord,
                    'serializer': PurineFoodRecordSerializer,
                },
                'uricAcid': {
                    'model': UricAcidRecord,
                    'serializer': UricAcidRecordSerializer,
                },
                'urinePH': {
                    'model': UrinePHRecord,
                    'serializer': UrinePHRecordSerializer,
                },
                'liverFunction': {
                    'model': LiverFunctionRecord,
                    'serializer': LiverFunctionRecordSerializer,
                },
                'kidneyFunction': {
                    'model': KidneyFunctionRecord,
                    'serializer': KidneyFunctionRecordSerializer,
                },
                'bloodSugar': {
                    'model': BloodSugarRecord,
                    'serializer': BloodSugarRecordSerializer,
                },
                'bloodPressure': {
                    'model': BloodPressureRecord,
                    'serializer': BloodPressureRecordSerializer,
                },
                'bloodLipid': {
                    'model': BloodLipidRecord,
                    'serializer': BloodLipidRecordSerializer,
                },
                'attack': {
                    'model': AttackRecord,
                    'serializer': AttackRecordSerializer,
                },
                'tophi': {
                    'model': TophiRecord,
                    'serializer': TophiRecordSerializer,
                },
                'surgery': {
                    'model': SurgeryRecord,
                    'serializer': SurgeryRecordSerializer,
                },
                'jointFunction': {
                    'model': JointFunctionRecord,
                    'serializer': JointFunctionRecordSerializer,
                },
            }
            
            # Process each record type
            for record_type, config in record_types.items():
                type_records = config['model'].objects.filter(record__in=records, record__record_type=record_type)
                if type_records.exists():
                    grouped_records[record_type] = config['serializer'](type_records, many=True).data
            
            return Response(grouped_records)
        except Exception as e:
            logger.error(f"Error fetching records: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request):
        try:
            logger.debug(f"POST record for user: {request.user.phone}")
            logger.debug(f"Received data: {json.dumps(request.data, default=str)}")
            
            record_type = request.data.get('record_type')
            date = request.data.get('date')
            data = request.data.get('data', {})
            
            if not record_type or not date:
                return Response(
                    {'error': 'record_type and date are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create base record
            record = Record(
                user=request.user,
                record_type=record_type,
                date=date
            )
            record.save()
            
            # Define handlers for each record type
            record_handlers = {
                'weight': self._handle_weight_record,
                'mainFood': self._handle_main_food_record,
                'waterIntake': self._handle_water_intake_record,
                'purineFood': self._handle_purine_food_record,
                'uricAcid': self._handle_uric_acid_record,
                'urinePH': self._handle_urine_ph_record,
                'liverFunction': self._handle_liver_function_record,
                'kidneyFunction': self._handle_kidney_function_record,
                'bloodSugar': self._handle_blood_sugar_record,
                'bloodPressure': self._handle_blood_pressure_record,
                'bloodLipid': self._handle_blood_lipid_record,
                'attack': self._handle_attack_record,
                'tophi': self._handle_tophi_record,
                'surgery': self._handle_surgery_record,
                'jointFunction': self._handle_joint_function_record,
            }
            
            # Get the appropriate handler for this record type
            handler = record_handlers.get(record_type)
            
            if handler:
                return handler(record, data)
            else:
                # If record_type is not recognized, delete the base record and return error
                record.delete()
                return Response(
                    {'error': f'Unsupported record_type: {record_type}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Exception as e:
            logger.error(f"Error creating record: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Handler methods for each record type
    def _handle_weight_record(self, record, data):
        value = data.get('value')
        if not value:
            record.delete()
            return Response({'error': 'Value is required for weight record'}, status=status.HTTP_400_BAD_REQUEST)
        
        weight_record = WeightRecord(record=record, value=value)
        weight_record.save()
        
        return Response(WeightRecordSerializer(weight_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_main_food_record(self, record, data):
        name = data.get('name')
        amount = data.get('amount')
        if not name or not amount:
            record.delete()
            return Response({'error': 'Name and amount are required for main food record'}, status=status.HTTP_400_BAD_REQUEST)
        
        main_food_record = MainFoodRecord(record=record, name=name, amount=amount)
        main_food_record.save()
        
        return Response(MainFoodRecordSerializer(main_food_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_water_intake_record(self, record, data):
        amount = data.get('amount', '')
        water_intake_record = WaterIntakeRecord(record=record, amount=amount)
        water_intake_record.save()
        
        return Response(WaterIntakeRecordSerializer(water_intake_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_purine_food_record(self, record, data):
        type_val = data.get('type', '')
        amount = data.get('amount', '')
        purine_food_record = PurineFoodRecord(record=record, type=type_val, amount=amount)
        purine_food_record.save()
        
        return Response(PurineFoodRecordSerializer(purine_food_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_uric_acid_record(self, record, data):
        value = data.get('value', '')
        method = data.get('method', '')
        uric_acid_record = UricAcidRecord(record=record, value=value, method=method)
        uric_acid_record.save()
        
        return Response(UricAcidRecordSerializer(uric_acid_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_urine_ph_record(self, record, data):
        value = data.get('value', '')
        urine_ph_record = UrinePHRecord(record=record, value=value)
        urine_ph_record.save()
        
        return Response(UrinePHRecordSerializer(urine_ph_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_liver_function_record(self, record, data):
        value = data.get('value', '')
        liver_function_record = LiverFunctionRecord(record=record, value=value)
        liver_function_record.save()
        
        return Response(LiverFunctionRecordSerializer(liver_function_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_kidney_function_record(self, record, data):
        value = data.get('value')
        if not value:
            record.delete()
            return Response({'error': 'Value is required for kidney function record'}, status=status.HTTP_400_BAD_REQUEST)
        
        kidney_function_record = KidneyFunctionRecord(record=record, value=value)
        kidney_function_record.save()
        
        return Response(KidneyFunctionRecordSerializer(kidney_function_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_blood_sugar_record(self, record, data):
        value = data.get('value')
        if not value:
            record.delete()
            return Response({'error': 'Value is required for blood sugar record'}, status=status.HTTP_400_BAD_REQUEST)
        
        blood_sugar_record = BloodSugarRecord(record=record, value=value)
        blood_sugar_record.save()
        
        return Response(BloodSugarRecordSerializer(blood_sugar_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_blood_pressure_record(self, record, data):
        value = data.get('value')
        if not value:
            record.delete()
            return Response({'error': 'Values are required for blood pressure record'}, status=status.HTTP_400_BAD_REQUEST)
        
        blood_pressure_record = BloodPressureRecord(record=record, value=value)
        blood_pressure_record.save()
        
        return Response(BloodPressureRecordSerializer(blood_pressure_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_blood_lipid_record(self, record, data):
        value = data.get('value')
        if not value:
            record.delete()
            return Response({'error': 'Values are required for blood lipid record'}, status=status.HTTP_400_BAD_REQUEST)
        
        blood_lipid_record = BloodLipidRecord(record=record, value=value)
        blood_lipid_record.save()
        
        return Response(BloodLipidRecordSerializer(blood_lipid_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_attack_record(self, record, data):
        pain_score = data.get('pain_score')
        duration = data.get('duration')
        if not pain_score or not duration:
            record.delete()
            return Response({'error': 'Pain score and duration are required for attack record'}, status=status.HTTP_400_BAD_REQUEST)
        
        attack_record = AttackRecord(record=record, pain_score=pain_score, duration=duration)
        attack_record.save()
        
        return Response(AttackRecordSerializer(attack_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_tophi_record(self, record, data):
        location = data.get('location')
        size = data.get('size')
        if not location or not size:
            record.delete()
            return Response({'error': 'Location and size are required for tophi record'}, status=status.HTTP_400_BAD_REQUEST)
        
        tophi_record = TophiRecord(record=record, location=location, size=size)
        tophi_record.save()
        
        return Response(TophiRecordSerializer(tophi_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_surgery_record(self, record, data):
        location = data.get('location')
        notes = data.get('notes', '')
        if not location:
            record.delete()
            return Response({'error': 'Location is required for surgery record'}, status=status.HTTP_400_BAD_REQUEST)
        
        surgery_record = SurgeryRecord(record=record, location=location, notes=notes)
        surgery_record.save()
        
        return Response(SurgeryRecordSerializer(surgery_record).data, status=status.HTTP_201_CREATED)
    
    def _handle_joint_function_record(self, record, data):
        joint = data.get('joint')
        description = data.get('description')
        if not joint or not description:
            record.delete()
            return Response({'error': 'Joint, description are required for joint function record'}, status=status.HTTP_400_BAD_REQUEST)
        
        joint_function_record = JointFunctionRecord(record=record, joint=joint, description=description)
        joint_function_record.save()
        
        return Response(JointFunctionRecordSerializer(joint_function_record).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, record_id=None):
        if not record_id:
            record_id = request.query_params.get('id')
            
        if not record_id:
            return Response(
                {'error': 'Record ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Deleting the base record will cascade delete the type-specific record
            record = Record.objects.get(id=record_id, user=request.user)
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Record.DoesNotExist:
            return Response(
                {'error': 'Record not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting record: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserRecordsViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get records for the current user
            records = UserRecordsView.objects.filter(user_id=request.user.id)
            
            # Apply date filtering if provided
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            record_type = request.query_params.get('record_type')
            
            if start_date:
                records = records.filter(date__gte=start_date)
            
            if end_date:
                records = records.filter(date__lte=end_date)
            
            if record_type:
                records = records.filter(record_type=record_type)
            
            # Paginate results
            paginator = PageNumberPagination()
            paginator.page_size = 50  # Adjust as needed
            result_page = paginator.paginate_queryset(records, request)
            
            serializer = UserRecordsViewSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error fetching user records view: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
