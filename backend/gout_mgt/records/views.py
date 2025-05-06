from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.auth import TokenAuthentication  # Use your custom TokenAuthentication
from .models import Record
from .serializers import RecordSerializer
import logging
import json

logger = logging.getLogger(__name__)

class RecordView(APIView):
    authentication_classes = [TokenAuthentication]  # Use your custom TokenAuthentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get all records for the user
            records = Record.objects.filter(user=request.user)
            
            # Group by record_type
            grouped_records = {}
            for record in records:
                if record.record_type not in grouped_records:
                    grouped_records[record.record_type] = []
                
                # Format the record data
                record_data = {
                    'id': record.id,
                    'date': record.date,
                    **record.data
                }
                grouped_records[record.record_type].append(record_data)
            
            return Response(grouped_records)
        except Exception as e:
            logger.error(f"Error fetching records: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            
            # Create new record
            record = Record(
                user=request.user,
                record_type=record_type,
                date=date,
                data=data
            )
            record.save()
            
            serializer = RecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error creating record: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, record_id=None):
        if not record_id:
            record_id = request.query_params.get('id')
            
        if not record_id:
            return Response(
                {'error': 'Record ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
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
