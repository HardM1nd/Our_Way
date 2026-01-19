from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserView, LogoutView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST /api/auth/token/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # POST /api/auth/token/refresh/
    path('register/', RegisterView.as_view(), name='auth_register'),         # POST /api/auth/register/
    path('user/', UserView.as_view(), name='auth_user'),                     # GET /api/auth/user/
    path('logout/', LogoutView.as_view(), name='auth_logout'),               # POST /api/auth/logout/
]