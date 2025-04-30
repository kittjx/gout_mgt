from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone')
        read_only_fields = ('id',)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

class RegistrationSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'verification_code')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data.pop('verification_code')
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user

class VerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
