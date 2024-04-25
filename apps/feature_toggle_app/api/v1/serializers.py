from rest_framework import serializers
from apps.feature_toggle_app.models import FeatureToggle

class FeatureToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureToggle
        fields = '__all__'  # Includes all fields of the model in the serializer.

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['state_value'] = instance.get_state_display()
        data['environment_value'] = instance.get_environment_display()
        data['state'] = instance.state
        data['environment'] = instance.environment
        data['notes'] = instance.notes or ""
        data['description'] = instance.description or ""

        return data