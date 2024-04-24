from django.urls import path
from . import views

urlpatterns = [ 
    path("list/", views.ToggleAPIView.as_view(), name="feature_toggle_list"),
    path("create/", views.ToggleAPIView.as_view(), name="feature_toggle_create"),
    path("detail/", views.FeatureToggleDetailAPIView.as_view(), name='feature_toggle_detail'),
    path("change-environment/", views.FeatureToggleChangeEnvironmentAPIView.as_view(), name="toggle_update"),
    path("activate-deactivate/", views.FeatureToggleActivateDeactivateAPIView.as_view(), name="toggle_enabled_disabled"),
]