from rest_framework import serializers

from .models import CustomUser
from .utils import send_activation_sms


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True,
                                     required=True)
    password_confirmation = serializers.CharField(min_length=8, write_only=True,
                                                  required=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'username',
                  'password', 'password_confirmation')

    def validate_phone_number(self, phone_number):
        if not phone_number.startswith('+996'):
            raise serializers.ValidationError('Use Kyrgyz number!')
        return phone_number

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirmation')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_sms(str(user.phone_number), user.activation_code)
        return user


