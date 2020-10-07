from django.urls import path
from Profile.views import LoginView,SignupView

app_name='account_app'
urlpatterns = [
    path('login/',LoginView,name="login"),
     path('signup/',SignupView.as_view(),name="signup")
]
