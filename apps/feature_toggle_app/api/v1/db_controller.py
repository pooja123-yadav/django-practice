from utils.network_helper.responses import RESPONSES, raise_error
from ...models import FeatureToggle 
from .serializers import FeatureToggleSerializer


def get_toggle_list_with_filters_db(filters):

    feature_toggles = FeatureToggle.objects.all()
    if filters:
        feature_toggles = feature_toggles.filter(**filters)

    # Serialize the filtered feature toggles
    serializer = FeatureToggleSerializer(feature_toggles, many=True)

    return serializer.data


def get_toggle_detail_db(identifier):

    try:
        feature_toggle = FeatureToggle.objects.get(identifier=identifier)
    except FeatureToggle.DoesNotExist:
        raise_error(RESPONSES.FeatureToggle.ERRORS.DOES_NOT_EXIST)

    serializer = FeatureToggleSerializer(feature_toggle)

    return serializer.data


def create_feature_toggle_db(post_data):
    serializer = FeatureToggleSerializer(data=post_data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise_error(RESPONSES.ERRORS.VALIDATIONS.TOGGLE_DATA_VALIDATION_FAILED, message=serializer.errors)


def bulk_update_toggle_state_db(ids, update_fields):
    if not ids:
        return False
    return FeatureToggle.objects.filter(id__in=ids).update(**update_fields)


def bulk_update_toggle_environment_db(ids, update_fields):
    if not ids:
        return False
    return FeatureToggle.objects.filter(id__in=ids).update(**update_fields)        