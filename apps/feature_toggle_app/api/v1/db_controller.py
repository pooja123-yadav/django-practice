from ...models import FeatureToggle 
from .serializers import FeatureToggleSerializer


def get_toggle_list_with_filters_db(filters):

    feature_toggles = FeatureToggle.objects.all()
    if filters:
        feature_toggles = feature_toggles.filter(**filters)

    # Serialize the filtered feature toggles
    serializer = FeatureToggleSerializer(feature_toggles, many=True)

    return serializer.data

def create_feature_toggle_db(post_data):
    serializer = FeatureToggleSerializer(data=post_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return "error"