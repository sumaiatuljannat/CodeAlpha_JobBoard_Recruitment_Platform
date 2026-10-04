from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.applications.models import JobApplication
from apps.candidates.models import CandidateProfile, Resume
from apps.employers.models import Company, EmployerProfile
from apps.jobs.models import Job
from apps.notifications.models import Notification


class RecruiterInterviewInvitationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.recruiter = User.objects.create_user(
            email='recruiter@example.com',
            password='test-password-123',
            first_name='Taylor',
            role=User.Role.EMPLOYER,
        )
        self.company = Company.objects.create(
            name='Interview Test Company',
            industry='Technology',
            headquarters='Remote',
            about='Test company',
        )
        EmployerProfile.objects.create(user=self.recruiter, company=self.company)
        self.candidate_user = User.objects.create_user(
            email='candidate@example.com',
            password='test-password-123',
            first_name='Jordan',
            last_name='Candidate',
            role=User.Role.CANDIDATE,
        )
        self.candidate = CandidateProfile.objects.create(user=self.candidate_user)
        self.job = Job.objects.create(
            company=self.company,
            posted_by=self.recruiter,
            title='Software Engineer',
            location='Remote',
            description='Build and maintain software.',
        )
        self.application = JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate,
        )

    def test_recruiter_can_invite_applicant_and_candidate_receives_message(self):
        self.client.force_authenticate(user=self.recruiter)

        response = self.client.patch(
            reverse('applications-change-status', kwargs={'pk': self.application.pk}),
            {'status': JobApplication.Status.INTERVIEW, 'note': 'Are you available Tuesday afternoon?'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, JobApplication.Status.INTERVIEW)
        notification = Notification.objects.get(recipient=self.candidate_user)
        self.assertEqual(notification.notification_type, Notification.NotificationType.INTERVIEW_INVITE)
        self.assertIn('selected for an interview', notification.message)
        self.assertIn('Tuesday afternoon', notification.message)

    def test_candidate_can_upload_cv(self):
        self.client.force_authenticate(user=self.candidate_user)

        response = self.client.post(
            reverse('candidate-resumes-list'),
            {
                'title': 'Jordan Candidate CV',
                'file': SimpleUploadedFile('candidate-cv.pdf', b'%PDF-1.4 test', content_type='application/pdf'),
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Resume.objects.filter(candidate=self.candidate).exists())

    def test_recruiter_cannot_upload_candidate_cv(self):
        self.client.force_authenticate(user=self.recruiter)

        response = self.client.post(
            reverse('candidate-resumes-list'),
            {
                'title': 'Unauthorized CV',
                'file': SimpleUploadedFile('unauthorized.pdf', b'%PDF-1.4 test', content_type='application/pdf'),
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Resume.objects.exists())