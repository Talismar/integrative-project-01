from django.urls import path

from sacm_pi_1.users.views import (
    user_login_view,
    user_logout_view
)

app_name = "users"
urlpatterns = [
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
]
