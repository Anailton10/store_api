from django.urls import path
from .views import UserRegisterView

urlpatterns = [
    path(
        'accounts/register/', view=UserRegisterView.as_view(), name='register'
    ),
]
