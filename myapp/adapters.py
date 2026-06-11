from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def get_login_redirect_url(self, request):
        user = request.user
        
        if user.is_authenticated:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            ref = str(refresh)
            
            frontend = "https://ai-code-mentor-frontend.onrender.com/dashboard"
            return f"{frontend}?access={access}&refresh={ref}"
        
        return "https://ai-code-mentor-frontend.onrender.com/login"