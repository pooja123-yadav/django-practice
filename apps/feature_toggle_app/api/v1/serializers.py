from rest_framework import serializers
from apps.feature_toggle_app.models import FeatureToggle

class FeatureToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureToggle
        fields = '__all__'  # Includes all fields of the model in the serializer.