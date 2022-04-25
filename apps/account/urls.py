from django.urls import path
from .views import RegisterView, LoadUserView

urlpatterns = [
    path('register/', RegisterView.as_view()), # api/account/register
    path('', LoadUserView.as_view()), # api/account/user

]