import django_filters
from django.db.models import Q
from apps.jobs.models import Job

class JobFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_by_keyword')
    category = django_filters.CharFilter(field_name='category__slug')
    category_id = django_filters.NumberFilter(field_name='category_id')
    company = django_filters.CharFilter(field_name='company__slug')
    company_id = django_filters.NumberFilter(field_name='company_id')
    employment_type = django_filters.CharFilter(field_name='employment_type')
    workplace_type = django_filters.CharFilter(field_name='workplace_type')
    experience_level = django_filters.CharFilter(field_name='experience_level')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    min_salary = django_filters.NumberFilter(field_name='min_salary', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='max_salary', lookup_expr='lte')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    skills = django_filters.CharFilter(method='filter_by_skills')

    class Meta:
        model = Job
        fields = [
            'keyword', 'category', 'category_id', 'company', 'company_id',
            'employment_type', 'workplace_type', 'experience_level', 'location',
            'min_salary', 'max_salary', 'is_featured', 'skills'
        ]

    def filter_by_keyword(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(company__name__icontains=value) |
            Q(job_skills__skill__name__icontains=value) |
            Q(location__icontains=value)
        ).distinct()

    def filter_by_skills(self, queryset, name, value):
        if not value:
            return queryset
        skills_list = [s.strip() for s in value.split(',') if s.strip()]
        return queryset.filter(job_skills__skill__name__in=skills_list).distinct()
