from rest_framework import serializers
from ..models import User
import pyotp

class VerifyMFASerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, allow_blank=False)

    def verify_mfa(self):
        try:
            userEmail = self.context.get('userEmail')  # Fixed incorrect variable access
            user = User.objects.filter(email=userEmail).first()

            if not user:
                return False  # User not found

            secret = user.mfa_secret  # Assuming user has an `mfa_secret` field

            if not secret or not pyotp.TOTP(secret).verify(self.validated_data['otp']):
                return False  # OTP is incorrect

            user.mfa_enabled = True
            user.save()
            return True  # OTP verified successfully

        except Exception as e:
            print("Error verifying MFA OTP:", e)
            return False
