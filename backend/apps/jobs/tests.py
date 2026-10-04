from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.employers.models import Company, EmployerProfile
from apps.jobs.models import Job, JobCategory
from apps.candidates.models import CandidateProfile
from apps.applications.models import JobApplication

class JobAndApplicationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer_user = User.objects.create_user(
            email='recruiter@apex.com',
            password='password123',
            first_name='Apex',
            last_name='Recruiter',
            role=User.Role.EMPLOYER
        )
        self.company = Company.objects.create(
            name='Apex Cloud Labs',
            industry='Software',
            headquarters='Remote',
            about='Next-gen cloud infrastructure'
        )
        EmployerProfile.objects.create(
            user=self.employer_user,
            company=self.company
        )

        self.candidate_user = User.objects.create_user(
            email='cand@dev.com',
            password='password123',
            first_name='Dev',
            last_name='Candidate',
            role=User.Role.CANDIDATE
        )
        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            headline='Senior Python Engineer'
        )

        self.category = JobCategory.objects.create(name='Engineering', icon='Code')
        self.job = Job.objects.create(
            company=self.company,
            posted_by=self.employer_user,
            title='Staff Backend Architect',
            category=self.category,
            employment_type='full_time',
            workplace_type='remote',
            location='Remote (US/EU)',
            min_salary=140000,
            max_salary=180000,
            description='Lead our distributed backend infrastructure team.',
            status=Job.Status.PUBLISHED
        )

    def test_public_job_search(self):
        url = reverse('jobs-list')
        res = self.client.get(url, {'search': 'Backend'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Results are paginated
        results = res.data.get('results', res.data)
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]['title'], 'Staff Backend Architect')

    def test_job_application_and_duplicate_prevention(self):
        self.client.force_authenticate(user=self.candidate_user)
        url = reverse('applications-list')
        app_data = {
            'job': self.job.id,
            'cover_letter': 'I am thrilled to apply for this backend architect position.'
        }
        res1 = self.client.post(url, app_data, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 1)

        # Attempt duplicate application
        res2 = self.client.post(url, app_data, format='json')
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(JobApplication.objects.count(), 1)
