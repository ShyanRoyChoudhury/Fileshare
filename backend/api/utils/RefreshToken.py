from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailTimestampRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        """
        Create a refresh token for the given user with additional claims.
        
        Args:
            user: The user instance to create token for
            
        Returns:
            RefreshToken: Token instance with custom claims
            
        Raises:
            ValueError: If user email is not set
        """
        if not user.email:
            logger.error(f"Attempted to create token for user without email: {user.id}")
            raise ValueError("User must have an email address to generate token")

        try:
            token = super().for_user(user)
            
            # Add custom claims
            token["email"] = user.email
            token["timestamp"] = int(timezone.now().timestamp())
            token["user_id"] = str(user.id)  # Add user ID for additional verification
            
            # Add any user-specific claims
            if hasattr(user, 'role'):
                token["role"] = user.role
                
            if hasattr(user, 'is_verified'):
                token["is_verified"] = user.is_verified
                
            # Add token metadata
            token["iat"] = datetime.utcnow().timestamp()  # Issued at time
            
            logger.info(f"Generated token for user: {user.email}")
            return token
            
        except Exception as e:
            logger.error(f"Error generating token for user {user.email}: {str(e)}")
            raise

    def verify(self):
        """
        Additional verification method to validate token claims.
        """
        super().verify()
        
        # Verify required claims are present
        if "email" not in self:
            raise self.token_type.token_class.error_class("Token has no email claim")
            
        if "timestamp" not in self:
            raise self.token_type.token_class.error_class("Token has no timestamp claim")