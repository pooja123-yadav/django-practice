# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.feature_toggle_app.models import FeatureToggle


class FeatureToggleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a feature toggle for testing
        FeatureToggle.objects.create(identifier='feature1', description='Feature 1', state=1, environment=1)
        FeatureToggle.objects.create(identifier='feature2', description='Feature 2', state=0, environment=2)


    def test_feature_toggle_list(self):
        url = reverse('feature_toggle_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming 2 feature toggles are created in setUp()


    def test_create_feature_toggle(self):
        url = reverse('feature_toggle_create')
        data = {'identifier': 'feature1', 'description': 'Feature 1', 'state': 1, 'environment': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # Negative Test Cases

    def test_feature_toggle_list_unauthorized(self):
        self.client.credentials()  # Clear authentication credentials
        url = reverse('feature_toggle_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_feature_toggle_unauthorized(self):
        self.client.credentials()  # Clear authentication credentials
        url = reverse('feature_toggle_create')
        data = {'identifier': 'feature1', 'description': 'Feature 1', 'state': 1, 'environment': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_feature_toggle_invalid_data(self):
        url = reverse('feature_toggle_create')
        invalid_data = {'identifier': ''}  # Missing required fields
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_feature_toggle_duplicate_data(self):
    #     url = reverse('feature_toggle_create')
    #     invalid_data = {'identifier': 'feature1', 'description': 'Feature 1', 'state': 1, 'environment': 1}
    #     response = self.client.post(url, invalid_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('identifier', response.data)  # Ensure the response contains an error message for the duplicate identifier


