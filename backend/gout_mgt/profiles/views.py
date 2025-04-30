from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.auth import TokenAuthentication
from .models import PatientProfile
from .serializers import PatientProfileSerializer

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):

        try:
            profile = PatientProfile.objects.get(user=request.user)
            serializer = PatientProfileSerializer(profile)
            return Response(serializer.data)
        except PatientProfile.DoesNotExist:
            #return Response(status=status.HTTP_404_NOT_FOUND)
            return Response({
                    "user": request.user.id,
                    "name": "",
                    "age": None,
                    "gender": "",
                    "height": None,
                    "weight": None,
                    "phone": request.user.phone
                })
    
    def post(self, request):

        try:
            # Try to get existing profile
            profile = PatientProfile.objects.get(user=request.user)
            serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        except PatientProfile.DoesNotExist:
            # Create new profile if it doesn't exist
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = PatientProfileSerializer(data=data)
        
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
