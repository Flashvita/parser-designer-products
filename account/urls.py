from django.urls import path
from account import views


urlpatterns = [
    path('users/registation/', views.UserCreateView.as_view({'create': 'post'})),

]