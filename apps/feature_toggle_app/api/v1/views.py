from .controller import get_feature_toggle_list, create_feature_toggle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from apps.feature_toggle_app.models import FeatureToggle 
from .serializers import FeatureToggleSerializer
from rest_framework.permissions import IsAuthenticated


class ToggleAPIView(APIView):

    permission_classes = [IsAuthenticated]   

    def get(self, request):
        # Extract filters from query parameters
        state = request.query_params.get('state')
        environment = request.query_params.get('environment')
       
        # Check if state is provided and if it's not an integer
        if state is not None and not isinstance(int(state), int):
            raise ValidationError("State parameter must be an integer.")

        # Check if environment is provided and if it's not an integer
        if environment is not None and not isinstance(int(environment), int):
            raise ValidationError("Environment parameter must be an integer.")

        filters = dict()
        if state is not None:
            filters.update({"state":state})
        if environment is not None:
            filters.update({"environment":environment})

        result = get_feature_toggle_list(filters)

        return Response(result)


    """
        Create a new feature toggle.

        Request Body:
        - identifier (string): Unique identifier for the feature toggle.
        - description (string): Description of the feature toggle.
        - state (boolean): Initial state of the feature toggle (enabled or disabled).

        Returns:
        - 201 Created: If the feature toggle is created successfully.
        - 400 Bad Request: If the request data is invalid.
    """

    def post(self, request):
        post_data = request.data
        post_data.update({"created_by": request.user.id}) 
        serializer = FeatureToggleSerializer(data=post_data)
        result = create_feature_toggle(post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FeatureToggleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]   
   
    def get(self, request):
        """
        Handle GET requests to retrieve details of a single feature toggle by its identifier.

        Parameters:
            request (Request): The HTTP request object.
            identifier (str): The identifier of the feature toggle to retrieve.

        Returns:
            Response: A JSON response containing the serialized feature toggle.
        """
        identifier = request.query_params.get('identifier')

        try:
            feature_toggle = FeatureToggle.objects.get(identifier=identifier)
        except FeatureToggle.DoesNotExist:
            raise NotFound("Feature toggle not found.")

        serializer = FeatureToggleSerializer(feature_toggle)
        return Response(serializer.data)