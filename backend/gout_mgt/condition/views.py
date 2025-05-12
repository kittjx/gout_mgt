from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.auth import TokenAuthentication
from .models import BasicCondition
from .serializers import BasicConditionSerializer
import logging

logger = logging.getLogger(__name__)

class BasicConditionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            basic_condition = BasicCondition.objects.filter(user=request.user).first()
            
            if not basic_condition:
                return Response({}, status=status.HTTP_200_OK)
            
            serializer = BasicConditionSerializer(basic_condition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving basic condition: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:
            # Check if basic condition already exists for this user
            basic_condition = BasicCondition.objects.filter(user=request.user).first()
            
            # Prepare data for serializer
            data = request.data.copy()
            
            # Transform limit_foods from list to limit_food_names
            if 'limit_foods' in data and isinstance(data['limit_foods'], list):
                data['limit_food_names'] = data.pop('limit_foods')
            
            # Transform complications and complication_dates to complication_data
            if 'complications' in data and isinstance(data['complications'], list):
                complications = data.pop('complications')
                complication_dates = data.pop('complication_dates', {}) or {}
                
                complication_data = []
                for comp_name in complications:
                    comp_data = {
                        'name': comp_name,
                        'diagnosis_date': complication_dates.get(comp_name)
                    }
                    complication_data.append(comp_data)
                
                data['complication_data'] = complication_data
            
            # Transform medicines to medicine_data
            if 'medicines' in data and isinstance(data['medicines'], list):
                data['medicine_data'] = data.pop('medicines')
            
            if basic_condition:
                # Update existing basic condition
                serializer = BasicConditionSerializer(basic_condition, data=data, partial=True)
            else:
                # Create new basic condition
                data['user'] = request.user.id
                serializer = BasicConditionSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error saving basic condition: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
