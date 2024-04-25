from django.urls import path
from . import views

urlpatterns = [ 
    path("list/", views.ToggleAPIView.as_view(), name="feature_toggle_list"),
    path("create/", views.ToggleAPIView.as_view(), name="feature_toggle_create"),
    path("detail/", views.ToggleDetailAPIView.as_view(), name='feature_toggle_detail'),
    path("change-environment/", views.ToggleChangeEnvironmentAPIView.as_view(), name="feature_toggle_change_environment"),
    path("enabled-disabled/", views.ToggleEnabledDisabledAPIView.as_view(), name="feature_toggle_enabled_disabled"),
]