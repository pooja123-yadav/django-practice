from utils.paginator_utils import get_paginated_response
from utils.network_helper.responses import RESPONSES, raise_error
from ...models import FeatureToggle 
from .serializers import FeatureToggleSerializer


def get_feature_toggle_list_with_filters_db(filters, page, limit):

    feature_toggles = FeatureToggle.objects.all()
    if filters:
        feature_toggles = feature_toggles.filter(**filters)

    # Adding pagination 
    paginated_response = get_paginated_response(feature_toggles, page, limit)
    # Serialize the filtered feature toggles
    serialized_object_list = FeatureToggleSerializer(paginated_response['object_list'], many=True)
    paginated_response['object_list'] = serialized_object_list.data

    return paginated_response


def get_feature_toggle_detail_db(identifier):

    try:
        feature_toggle = FeatureToggle.objects.get(identifier=identifier, is_deleted= False)
    except FeatureToggle.DoesNotExist:
        raise_error(RESPONSES.FeatureToggle.ERRORS.DOES_NOT_EXIST)

    # Serialize the filtered feature toggle detail
    serializer = FeatureToggleSerializer(feature_toggle)

    return serializer.data


def create_feature_toggle_db(post_data):
    serializer = FeatureToggleSerializer(data=post_data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise_error(RESPONSES.ERRORS.VALIDATIONS.TOGGLE_DATA_VALIDATION_FAILED, message=serializer.errors)


def bulk_update_state_db(ids, update_fields):
    return FeatureToggle.objects.filter(id__in=ids).update(**update_fields)


def bulk_update_environment_db(ids, update_fields):
    return FeatureToggle.objects.filter(id__in=ids).update(**update_fields)        