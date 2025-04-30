import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, RegistrationSerializer, VerificationCodeSerializer
from .tokens import Token

# Simple in-memory store for verification codes (in production, use Redis or similar)
verification_codes = {}

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                phone=serializer.validated_data['phone'],
                password=serializer.validated_data['password']
            )
            
            if user:
                # Create or get token
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            return Response(
                {'error': '手机号或密码不正确'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verification_code = serializer.validated_data['verification_code']
            
            # Check if verification code is valid
            if verification_codes.get(phone) != verification_code:
                return Response(
                    {'error': '验证码不正确'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create user
            user = serializer.save()
            
            # Create token
            token = Token.objects.create(user=user)
            
            # Clean up verification code
            if phone in verification_codes:
                del verification_codes[phone]
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationCodeView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            
            # Generate a 6-digit verification code
            code = ''.join(random.choices('0123456789', k=6))
            
            # Store the code (in a real app, send via SMS)
            verification_codes[phone] = code
            
            # Return the code directly (in production, don't return the code)
            return Response({'code': code}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
