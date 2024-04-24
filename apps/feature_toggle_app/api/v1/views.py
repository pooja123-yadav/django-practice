from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from apps.feature_toggle_app.models import FeatureToggle 
from .serializers import FeatureToggleSerializer
from rest_framework.permissions import IsAuthenticated
from utils.network_helper.responses import raise_error, RESPONSES, prepare_response
from .controller import get_feature_toggle_list, create_feature_toggle, get_feature_toggle_detail_by_identifier, bulk_update_toggle_state, bulk_update_toggle_environment

class ToggleAPIView(APIView):

    permission_classes = [IsAuthenticated]   

    def get(self, request):
        # Extract filters from query parameters
        state = request.query_params.get('state')
        environment = request.query_params.get('environment')

        # Check if state is provided and if it's not an integer
        if state is not None:
            try:
                state = int(state)
            except ValueError:
                raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_STATE)

        # Check if environment is provided and if it's not an integer
        if environment is not None:
            try:
                state = int(environment)
            except ValueError:
                raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ENVIRONMENT)
        
        filters = dict()
        if state is not None:
            filters.update({"state":state})
        if environment is not None:
            filters.update({"environment":environment})

        result = get_feature_toggle_list(filters)

        return prepare_response(data=result)
        

    def post(self, request):
        post_data = request.data
        post_data.update({"created_by": request.user.id}) 
        create_feature_toggle(data=post_data)
        return prepare_response(response=RESPONSES.GENERIC.CREATED, data=[])


class FeatureToggleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]   
   
    def get(self, request):
       
        identifier = request.query_params.get('identifier')

        if not identifier:
            raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_TOGGLE_IDENTIFIER)

        result = get_feature_toggle_detail_by_identifier(identifier=identifier)
        
        return prepare_response(data=result)
    

class FeatureToggleActivateDeactivateAPIView(APIView):

    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        body = request.data
        toggle_ids = body.get('ids', [])
        toggle_state_status = body.get('state')

        if not toggle_ids or (not isinstance(toggle_ids, list)):
            raise_error(RESPONSES.ERRORS.VALIDATIONS.ID_LIST_REQUIRED)

        if toggle_state_status is None:
            raise_error(
                RESPONSES.ERRORS.VALIDATIONS.INVALID_ACTIVE_INACTIVE_STATUS)
          
        metadata = {"updated_by": request.user.id}

        if body.get('notes'):
            metadata['notes'] = body.get('notes')

        status_updated_count = bulk_update_toggle_state(toggle_ids=toggle_ids, state=toggle_state_status, metadata=metadata)

        return prepare_response(RESPONSES.GENERIC.SUCCESS, data=status_updated_count)
    

class FeatureToggleChangeEnvironmentAPIView(APIView):

    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        body = request.data
        toggle_ids = body.get('ids', [])
        environment = body.get('environment')

        if not toggle_ids or (not isinstance(toggle_ids, list)):
            raise_error(RESPONSES.ERRORS.VALIDATIONS.ID_LIST_REQUIRED)

        if environment is None:
            raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ACTIVE_INACTIVE_STATUS)

        metadata = {"updated_by": request.user.id}

        if body.get('notes'):
            metadata['notes'] = body.get('notes')

        environment_updated_count = bulk_update_toggle_environment(toggle_ids=toggle_ids, environment=environment, metadata=metadata)

        return prepare_response(RESPONSES.GENERIC.SUCCESS, data=environment_updated_count)

