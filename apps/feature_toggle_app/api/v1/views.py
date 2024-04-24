from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from apps.feature_toggle_app.models import FeatureToggle 
from .serializers import FeatureToggleSerializer
from rest_framework.permissions import IsAuthenticated
from utils.network_helper.responses import raise_error, RESPONSES, prepare_response
from .controller import get_feature_toggle_list


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
        
        # Filter feature toggles based on query parameters
        # feature_toggles = FeatureToggle.objects.all()
        # if state is not None:
        #     feature_toggles = feature_toggles.filter(state=state)
        # if environment is not None:
        #     feature_toggles = feature_toggles.filter(environment=environment)

        # # Serialize the filtered feature toggles
        # serializer = FeatureToggleSerializer(feature_toggles, many=True)
        result = get_feature_toggle_list()
        return prepare_response(data=serializer.data)
        

    def post(self, request):
        post_data = request.data
        post_data.update({"created_by": request.user.id}) 
        serializer = FeatureToggleSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FeatureToggleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]   
   
    def get(self, request):
       
        identifier = request.query_params.get('identifier')

        try:
            feature_toggle = FeatureToggle.objects.get(identifier=identifier)
        except FeatureToggle.DoesNotExist:
            raise NotFound("Feature toggle not found.")

        serializer = FeatureToggleSerializer(feature_toggle)
        return Response(serializer.data)