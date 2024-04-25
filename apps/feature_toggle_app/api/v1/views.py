from utils.network_helper.request_utils import get_validated_request_body
from utils.network_helper.responses import raise_error, RESPONSES, prepare_response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .controller import get_feature_toggle_list, create_feature_toggle, get_feature_toggle_detail_by_identifier, bulk_update_feature_toggle_state, bulk_update_feature_toggle_environment
from apps.feature_toggle_app.models import FeatureToggle


class ToggleAPIView(APIView):

    permission_classes = [IsAuthenticated]   
    '''
        API to get feature Toggle List with filters 
    '''
    def get(self, request):

        # Extract filters from query parameters
        state = request.query_params.get('state')
        environment = request.query_params.get('environment')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

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
        
        # Prepare filters
        filters = dict()
        if state is not None:
            filters.update({"state":state})
        if environment is not None:
            filters.update({"environment":environment})
            
        # getting feature toggle list
        result = get_feature_toggle_list(filters, page, limit)

        return prepare_response(data=result)
        
    '''
        API to create feature Toggle 
    '''
    def post(self, request):

        # validating and getting post data to create feature toggle
        post_data = get_validated_request_body(request)

        # checking valid state value from model state choices
        if post_data.get('state'):
            valid_choices = [choice[0] for choice in FeatureToggle.TOGGLE_STATE.choices] 
            if post_data.get('state') not in valid_choices:
                raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ACTIVE_INACTIVE_STATUS)

        # checking valid environment values from model environment choices
        if post_data.get('environment'):
            valid_choices = [choice[0] for choice in FeatureToggle.ENVIRONMENT_LEVELS.choices] 
            if post_data.get('environment') not in valid_choices:
                raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ENVIRONMENT_LEVEL_VALUE)

        post_data.update({"created_by": request.user.id}) # adding login user id

        create_feature_toggle(data=post_data) # create feature toggle
        return prepare_response(response=RESPONSES.GENERIC.CREATED, data=[])


class ToggleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]  

    '''
        API to get Feature Toggle Details by Identifier name
    ''' 
    def get(self, request):
        # extract identifier from query params
        identifier = request.query_params.get('identifier')

        # If identifier has no value
        if not identifier:
            raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_TOGGLE_IDENTIFIER)

        # Getting Feature Toggle details from db
        result = get_feature_toggle_detail_by_identifier(identifier=identifier)
        
        return prepare_response(data=result)
    

class ToggleEnabledDisabledAPIView(APIView):

    permission_classes = [IsAuthenticated]  

    ''' 
        API to update Feature Toggle state enabled to disabled or vice-versa
    '''

    def post(self, request, *args, **kwargs):
        
        # validating and getting post data to create feature toggle
        body = get_validated_request_body(request) 
        toggle_ids = body.get('ids', [])
        toggle_state_status = body.get('state')

        # Checking if toggle ids are provided 
        if not toggle_ids or (not isinstance(toggle_ids, list)):
            raise_error(RESPONSES.ERRORS.VALIDATIONS.ID_LIST_REQUIRED)

        # validation if toggle state has no value
        if toggle_state_status is None:
            raise_error(
                RESPONSES.ERRORS.VALIDATIONS.INVALID_ACTIVE_INACTIVE_STATUS)
            
        # checking valid state value from model state choices
        if toggle_state_status:
            valid_choices = [choice[0] for choice in FeatureToggle.TOGGLE_STATE.choices] 
            if toggle_state_status not in valid_choices:
                raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ACTIVE_INACTIVE_STATUS)

        metadata = {"updated_by": request.user.id}

        if body.get('notes'):
            metadata['notes'] = body.get('notes')

        status_updated_count = bulk_update_feature_toggle_state(toggle_ids=toggle_ids, state=toggle_state_status, metadata=metadata)

        return prepare_response(RESPONSES.GENERIC.SUCCESS, data=status_updated_count)
    

class ToggleChangeEnvironmentAPIView(APIView):

    permission_classes = [IsAuthenticated]  

    ''' 
        API to update Feature Toggle environment (Global/Development/Production)
    '''
    def post(self, request, *args, **kwargs):

        # validating and getting post data to create feature toggle
        body = get_validated_request_body(request)        
        toggle_ids = body.get('ids', [])
        environment = body.get('environment')

        # Checking if toggle ids are provided
        if not toggle_ids or (not isinstance(toggle_ids, list)):
            raise_error(RESPONSES.ERRORS.VALIDATIONS.ID_LIST_REQUIRED)

        # validation if toggle environment has no value
        if environment is None:
            raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ENVIRONMENT_LEVEL_VALUE)

        # checking valid environment values from model environment choices
        if environment:
            valid_choices = [choice[0] for choice in FeatureToggle.ENVIRONMENT_LEVELS.choices] 
            if environment not in valid_choices:
                raise_error(RESPONSES.ERRORS.VALIDATIONS.INVALID_ENVIRONMENT_LEVEL_VALUE)

        metadata = {"updated_by": request.user.id}

        if body.get('notes'):
            metadata['notes'] = body.get('notes')

        environment_updated_count = bulk_update_feature_toggle_environment(toggle_ids=toggle_ids, environment=environment, metadata=metadata)

        return prepare_response(RESPONSES.GENERIC.SUCCESS, data=environment_updated_count)

