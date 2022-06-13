from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class TestRoomPhotoListAPIView(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='secret',
            username='user'
        )

    def test_not_sign_in_user(self):
        response = self.client.get('/api/v1/room-photos/', format='json')
        print(response.data)
