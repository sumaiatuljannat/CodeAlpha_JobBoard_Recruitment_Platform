from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User

class AccountsAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.candidate_data = {
            'email': 'john.doe@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'candidate'
        }
        self.employer_data = {
            'email': 'recruiter@techcorp.com',
            'password': 'password123',
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'role': 'employer',
            'company_name': 'TechCorp Systems'
        }

    def test_candidate_registration_and_profile_creation(self):
        url = reverse('auth-register')
        res = self.client.post(url, self.candidate_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data['success'])
        self.assertIn('access', res.data)
        
        user = User.objects.get(email='john.doe@example.com')
        self.assertEqual(user.role, User.Role.CANDIDATE)
        self.assertTrue(hasattr(user, 'candidate_profile'))

    def test_employer_registration_and_company_creation(self):
        url = reverse('auth-register')
        res = self.client.post(url, self.employer_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(email='recruiter@techcorp.com')
        self.assertEqual(user.role, User.Role.EMPLOYER)
        self.assertTrue(hasattr(user, 'employer_profile'))
        self.assertEqual(user.employer_profile.company.name, 'TechCorp Systems')

    def test_login_flow(self):
        # Create user
        User.objects.create_user(
            email='alice@example.com',
            password='mypassword123',
            first_name='Alice',
            last_name='Smith',
            role=User.Role.CANDIDATE
        )
        url = reverse('auth-login')
        res = self.client.post(url, {'email': 'alice@example.com', 'password': 'mypassword123'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_demo_login(self):
        url = reverse('auth-demo-login')
        res = self.client.post(url, {'role': 'candidate'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertEqual(res.data['user']['role'], 'candidate')

    def test_password_recovery(self):
        User.objects.create_user(
            email='recover@example.com',
            password='oldpassword',
            first_name='Recover',
            last_name='Test',
            role=User.Role.CANDIDATE
        )
        req_url = reverse('auth-password-reset-request')
        res1 = self.client.post(req_url, {'email': 'recover@example.com'}, format='json')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        confirm_url = reverse('auth-password-reset-confirm')
        res2 = self.client.post(confirm_url, {'email': 'recover@example.com', 'new_password': 'brandnewpassword'}, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

        # Try logging in with new password
        login_res = self.client.post(reverse('auth-login'), {'email': 'recover@example.com', 'password': 'brandnewpassword'}, format='json')
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
