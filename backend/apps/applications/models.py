from django.db import models
from apps.accounts.models import User
from apps.jobs.models import Job
from apps.candidates.models import CandidateProfile, Resume

class JobApplication(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'applied', 'Applied'
        SCREENING = 'screening', 'Under Review'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        INTERVIEW = 'interview', 'Interview'
        ASSESSMENT = 'assessment', 'Assessment'
        OFFER = 'offer', 'Offer Made'
        HIRED = 'hired', 'Hired'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    cover_letter = models.TextField(blank=True, default='')
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    availability_notice = models.CharField(max_length=100, blank=True, default='Immediate (2 weeks notice)')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.APPLIED, db_index=True)
    match_score = models.PositiveIntegerField(default=0)
    match_reasons = models.JSONField(default=list, blank=True)
    rejection_reason = models.TextField(blank=True)
    withdrawal_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'candidate')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} -> {self.job.title} ({self.status})"

    def calculate_match_score(self):
        """Calculate relevance score between candidate and job"""
        score = 0
        reasons = []
        
        # 1. Skills match (up to 50%)
        job_skills = set(self.job.job_skills.values_list('skill_id', flat=True))
        candidate_skills = set(self.candidate.skills.values_list('skill_id', flat=True))
        
        if job_skills:
            matched_skills = job_skills.intersection(candidate_skills)
            skill_ratio = len(matched_skills) / len(job_skills)
            skill_score = int(skill_ratio * 50)
            score += skill_score
            if len(matched_skills) > 0:
                reasons.append(f"{len(matched_skills)} of {len(job_skills)} required/preferred skills matched")
        else:
            score += 30
            reasons.append("Skills profile aligned with job requirements")

        # 2. Experience level match (up to 25%)
        cand_exp = self.candidate.experience_years
        job_level = self.job.experience_level
        
        level_map = {
            Job.ExperienceLevel.ENTRY: 0,
            Job.ExperienceLevel.JUNIOR: 1,
            Job.ExperienceLevel.MID: 3,
            Job.ExperienceLevel.SENIOR: 5,
            Job.ExperienceLevel.LEAD: 8,
            Job.ExperienceLevel.EXECUTIVE: 10,
        }
        min_required_exp = level_map.get(job_level, 2)
        if cand_exp >= min_required_exp:
            score += 25
            reasons.append(f"Experience requirement satisfied ({cand_exp}+ years)")
        else:
            partial_exp = int((cand_exp / max(1, min_required_exp)) * 20)
            score += partial_exp
            reasons.append(f"Developing experience for {self.job.get_experience_level_display()}")

        # 3. Location / Workplace type match (up to 15%)
        if self.job.workplace_type == Job.WorkplaceType.REMOTE or self.job.location.lower() in self.candidate.preferred_location.lower() or 'remote' in self.candidate.preferred_location.lower():
            score += 15
            reasons.append(f"Location preference matched ({self.job.location} / {self.job.get_workplace_type_display()})")
        else:
            score += 5

        # 4. Profile strength bonus (up to 10%)
        score += int((self.candidate.profile_strength / 100) * 10)

        final_score = min(98, max(45, score))
        self.match_score = final_score
        self.match_reasons = reasons
        self.save(update_fields=['match_score', 'match_reasons'])
        return final_score


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    note = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_status} -> {self.to_status} at {self.created_at}"


class RecruiterNote(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='recruiter_notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.author.get_full_name()} on App #{self.application_id}"
