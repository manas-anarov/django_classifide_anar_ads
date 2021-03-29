from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from restaccounts.models import ExtendedUser

CREATE_USER_URL = reverse('restaccounts:register')

def create_user(**params):
	return ExtendedUser.objects.create_user(**params)


class PublicUserApiTests(TestCase):
	"Test the users API (public)"

	def setUp(self):
		self.client = APIClient()

	def test_create_valid_user_success(self):
		"Test user valid payload"

		payload = {
			'username':' sasasdasd',
			'email': ' asdasasd@sd.ru',
			'password': 'q11111111',
		}
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		user = ExtendedUser.objects.get(**res.data)
		self.assertTrue(user.check_password(payload['password']))
		# self.assertNotIn('password', res.data)


	def test_user_exists(self):
		payload = {
			'username':'sasasdasd',
			'email':' asdasasd@sd.ru',
			'password': 'q11111111',
		}
		create_user(**payload)
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_user_password_too_short(self):
		payload = {
			'username':'sasasdasd',
			'email':' asdasasd@sd.ru',
			'password': 'q1',
		}
		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

		# user = DriverUser.objects.get(**res.data)
		# self.assertTrue(user.check_password(payload['password']))