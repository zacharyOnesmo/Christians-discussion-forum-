from django.urls import path

from .views import claim_detail_view, dashboard_view, login_view, logout_view, profile_view, register_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("claims/<int:claim_id>/", claim_detail_view, name="claim_detail"),
    path("", dashboard_view, name="dashboard"),
]
