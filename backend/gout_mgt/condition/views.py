from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.auth import TokenAuthentication
from .models import BasicCondition
from .serializers import BasicConditionSerializer

import logging
import json

logger = logging.getLogger(__name__)

class BasicConditionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            condition = BasicCondition.objects.get(user=request.user)
            serializer = BasicConditionSerializer(condition)
            return Response(serializer.data)
        except BasicCondition.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            logger.info(f"POST request for user: {request.user.phone}")
            logger.info(f"Received data: {json.dumps(request.data, default=str)}")

            condition, created = BasicCondition.objects.get_or_create(user=request.user)
            serializer = BasicConditionSerializer(condition, data=request.data, partial=True)
            
            if serializer.is_valid():
                logger.info(f"Validated data: {json.dumps(serializer.validated_data, default=str)}")
                instance = serializer.save()
                logger.info(f"Saved instance data: {json.dumps(BasicConditionSerializer(instance).data, default=str)}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
