import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User, AuditLog
from apps.employers.models import Company, EmployerProfile, CompanyVerification
from apps.jobs.models import JobCategory, Skill, Job, JobSkill, JobReport
from apps.candidates.models import (
    CandidateProfile,
    Education,
    Experience,
    CandidateSkill,
    Project,
    Certification,
    Resume,
    ResumeBuilder,
    SavedJob,
    JobAlert
)
from apps.applications.models import JobApplication, ApplicationStatusHistory, RecruiterNote
from apps.interviews.models import Interview
from apps.messaging.models import Conversation, Message
from apps.notifications.models import Notification, NotificationPreference

class Command(BaseCommand):
    help = 'Seeds database with 20+ companies, 100+ jobs, candidates, applications, and full recruitment workflows'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[+] Starting database seeding..."))

        # 1. Clean existing records (optional for fresh seed)
        # 2. Categories
        categories_data = [
            {'name': 'Software Engineering', 'icon': 'Code', 'description': 'Full-stack, frontend, backend, mobile, and systems engineering.', 'is_popular': True},
            {'name': 'Data Science & AI', 'icon': 'Brain', 'description': 'Machine learning, AI research, data analytics, and LLM engineering.', 'is_popular': True},
            {'name': 'Product & Design', 'icon': 'Palette', 'description': 'UI/UX design, product management, design systems, and user research.', 'is_popular': True},
            {'name': 'DevOps & Cloud', 'icon': 'Cloud', 'description': 'AWS, GCP, Kubernetes, CI/CD pipelines, and SRE.', 'is_popular': True},
            {'name': 'Cybersecurity', 'icon': 'Shield', 'description': 'Information security, penetration testing, compliance, and SOC.', 'is_popular': True},
            {'name': 'Marketing & Growth', 'icon': 'TrendingUp', 'description': 'Product marketing, SEO, content strategy, and performance growth.', 'is_popular': False},
            {'name': 'Finance & Operations', 'icon': 'DollarSign', 'description': 'Financial analysis, accounting, operations, and business strategy.', 'is_popular': False},
            {'name': 'Sales & Customer Success', 'icon': 'Users', 'description': 'Enterprise sales, account management, and client support.', 'is_popular': False},
            {'name': 'Healthcare & Biotech', 'icon': 'HeartPulse', 'description': 'Health informatics, bioinformatics, and medical software.', 'is_popular': False},
            {'name': 'Hardware & Embedded', 'icon': 'Cpu', 'description': 'Firmware, IoT devices, robotics, and embedded systems.', 'is_popular': False},
        ]
        
        category_objs = {}
        for cat in categories_data:
            c, _ = JobCategory.objects.get_or_create(
                name=cat['name'],
                defaults={'icon': cat['icon'], 'description': cat['description'], 'is_popular': cat['is_popular']}
            )
            category_objs[cat['name']] = c

        # 3. Skills
        skills_data = [
            ('Python', 'Software Engineering', True),
            ('Django', 'Software Engineering', True),
            ('React.js', 'Software Engineering', True),
            ('TypeScript', 'Software Engineering', True),
            ('Node.js', 'Software Engineering', True),
            ('Go / Golang', 'Software Engineering', True),
            ('PostgreSQL', 'Software Engineering', True),
            ('GraphQL', 'Software Engineering', False),
            ('Next.js', 'Software Engineering', True),
            ('Tailwind CSS', 'Software Engineering', True),
            ('Docker', 'DevOps & Cloud', True),
            ('Kubernetes', 'DevOps & Cloud', True),
            ('AWS', 'DevOps & Cloud', True),
            ('GCP', 'DevOps & Cloud', False),
            ('Terraform', 'DevOps & Cloud', True),
            ('CI/CD Pipelines', 'DevOps & Cloud', True),
            ('Machine Learning', 'Data Science & AI', True),
            ('PyTorch', 'Data Science & AI', True),
            ('TensorFlow', 'Data Science & AI', False),
            ('Large Language Models (LLMs)', 'Data Science & AI', True),
            ('Data Analysis', 'Data Science & AI', True),
            ('Pandas & NumPy', 'Data Science & AI', False),
            ('Figma', 'Product & Design', True),
            ('UI/UX Design', 'Product & Design', True),
            ('Design Systems', 'Product & Design', True),
            ('User Research', 'Product & Design', False),
            ('Product Strategy', 'Product & Design', True),
            ('Penetration Testing', 'Cybersecurity', True),
            ('SOC Analysis', 'Cybersecurity', False),
            ('Zero Trust Architecture', 'Cybersecurity', True),
            ('Agile / Scrum', 'Management', True),
        ]
        
        skill_objs = {}
        for s_name, s_cat, s_trend in skills_data:
            sk, _ = Skill.objects.get_or_create(
                name=s_name,
                defaults={'category': s_cat, 'is_trending': s_trend}
            )
            skill_objs[s_name] = sk

        # 4. Create Demo Admin
        admin_user, _ = User.objects.get_or_create(
            email='admin@hiresphere.io',
            defaults={
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_email_verified': True,
                'bio': 'Platform Super Admin & Safety Moderator'
            }
        )
        admin_user.set_password('demo123456')
        admin_user.save()

        # 5. Companies Data (22 Companies)
        companies_seed = [
            {
                'name': 'Apex Global Technologies',
                'industry': 'Enterprise Software & Cloud',
                'size': '501-1000',
                'founded': 2016,
                'headquarters': 'San Francisco, CA (Remote-first)',
                'website': 'https://apextech.example.com',
                'about': 'Apex Global Technologies builds next-generation distributed enterprise platforms trusted by Fortune 500 companies worldwide.',
                'mission': 'Empowering organizations to scale seamlessly through resilient cloud-native infrastructure.',
                'benefits': ['Comprehensive Health & Dental', '$3,000 Annual Learning Stipend', 'Unlimited PTO', 'Home Office Budget ($1,500)', '401(k) 6% Match'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'NeuroVanguard AI Labs',
                'industry': 'Artificial Intelligence & Robotics',
                'size': '51-200',
                'founded': 2021,
                'headquarters': 'Boston, MA',
                'website': 'https://neurovanguard.example.com',
                'about': 'Pioneering multimodal foundational models for autonomous agents, medical diagnostics, and spatial computing.',
                'mission': 'Advancing safe artificial general intelligence to augment human potential.',
                'benefits': ['Top 1% Competitive Equity', 'State of the art H100 compute cluster access', 'Daily Catered Gourmet Lunch', 'Comprehensive Wellness Plan'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'CloudScale Dynamics',
                'industry': 'DevOps & SRE',
                'size': '201-500',
                'founded': 2018,
                'headquarters': 'Seattle, WA',
                'website': 'https://cloudscaledynamics.example.com',
                'about': 'Autonomous Kubernetes optimization and multicloud observability platform.',
                'mission': 'Eliminate cloud outages and reduce cloud waste with AI-driven operations.',
                'benefits': ['100% Remote Flexibility', 'Flexible Working Hours', 'Quarterly Team Offsites', 'Stock Options'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'CyberSentinel Security',
                'industry': 'Cybersecurity & Defense',
                'size': '201-500',
                'founded': 2017,
                'headquarters': 'Austin, TX',
                'website': 'https://cybersentinel.example.com',
                'about': 'Zero-trust endpoint detection, identity security, and automated cloud incident response systems.',
                'mission': 'Securing the global digital frontier against state-sponsored and advanced cyber threats.',
                'benefits': ['Security Certification Sponsorship', 'Parental Leave (16 weeks)', 'Health & Life Insurance', 'Generous Bonus Scheme'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Starlight Fintech',
                'industry': 'Financial Technology',
                'size': '501-1000',
                'founded': 2019,
                'headquarters': 'New York, NY',
                'website': 'https://starlightfintech.example.com',
                'about': 'Real-time cross-border payment networks and high-frequency algorithmic trade infrastructure.',
                'mission': 'Making global money movement instant, borderless, and virtually free.',
                'benefits': ['Competitive Wall St Compensation', 'Annual Discretionary Bonus', 'Gym & Fitness Membership', 'Retirement 401(k) Matching'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'PulseBio Therapeutics',
                'industry': 'Healthcare & Biotech',
                'size': '51-200',
                'founded': 2020,
                'headquarters': 'Cambridge, MA',
                'website': 'https://pulsebio.example.com',
                'about': 'Accelerating precision oncology and computational drug discovery using generative biological models.',
                'mission': 'Curing complex diseases by decoding human cellular dynamics.',
                'benefits': ['High-impact lifesaving mission', 'Comprehensive Health Plan', 'Patent Reward Incentives'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'QuantumUX Studio',
                'industry': 'Design & Product Innovation',
                'size': '11-50',
                'founded': 2022,
                'headquarters': 'London, UK (Remote)',
                'website': 'https://quantumux.example.com',
                'about': 'Award-winning product design and design systems consultancy crafting world-class digital experiences.',
                'mission': 'Crafting delightful, accessible, and intuitive software interfaces.',
                'benefits': ['4-day Work Week (32 hrs)', 'MacBook Pro M3 Max provided', 'Annual design retreat in Europe'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1572044162444-ad60f128bdea?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'HyperFlow Data',
                'industry': 'Big Data & Analytics',
                'size': '201-500',
                'founded': 2018,
                'headquarters': 'Berlin, Germany',
                'website': 'https://hyperflow.example.com',
                'about': 'Ultra high-throughput event streaming and distributed real-time analytical query engine.',
                'mission': 'Turning streaming data into actionable business intelligence in milliseconds.',
                'benefits': ['Relocation Assistance', 'German & English language courses', 'Subsidized Public Transit Pass'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Zenith E-Commerce Solutions',
                'industry': 'E-Commerce & Retail Tech',
                'size': '501-1000',
                'founded': 2015,
                'headquarters': 'Chicago, IL',
                'website': 'https://zenithecom.example.com',
                'about': 'Headless commerce infrastructure powering millions of checkouts for global consumer brands.',
                'mission': 'Empowering direct-to-consumer retailers with lightning-fast frictionless checkout.',
                'benefits': ['Merchandise Discounts', 'Full Health & Vision', 'Work-from-anywhere policy'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1556742049-0a67e55722c0?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'NovaLink Networks',
                'industry': 'Telecommunications & 5G',
                'size': '1000+',
                'founded': 2012,
                'headquarters': 'Toronto, Canada',
                'website': 'https://novalink.example.com',
                'about': 'Next-generation satellite mesh networking and distributed edge computing hubs.',
                'mission': 'Connecting the next 3 billion people with high-speed low-latency broadband.',
                'benefits': ['Defined Benefit Pension Plan', 'Tuition Reimbursement', 'On-site Gym & Childcare'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'GreenGrid Energy Tech',
                'industry': 'CleanTech & Renewable Energy',
                'size': '51-200',
                'founded': 2020,
                'headquarters': 'Stockholm, Sweden',
                'website': 'https://greengrid.example.com',
                'about': 'Smart grid battery storage balancing software and virtual power plant optimization.',
                'mission': 'Accelerating the 100% renewable energy transition with predictive AI.',
                'benefits': ['Electric Vehicle Lease Subsidy', '6 Weeks Vacation', 'Sustainable Pension Fund'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'AeroDynamics Autonomous Systems',
                'industry': 'Aerospace & Robotics',
                'size': '201-500',
                'founded': 2017,
                'headquarters': 'Boulder, CO',
                'website': 'https://aerodynamics.example.com',
                'about': 'Autonomous drone logistics fleet for medical supply deliveries and disaster response.',
                'mission': 'Saving lives through reliable aerial robotics delivery.',
                'benefits': ['Ski pass stipend', 'Comprehensive healthcare', 'Flight simulator access'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1519074069444-1ba4ea16e91f?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Kinetix Health AI',
                'industry': 'Digital Health & Telemedicine',
                'size': '51-200',
                'founded': 2021,
                'headquarters': 'San Diego, CA',
                'website': 'https://kinetixhealth.example.com',
                'about': 'AI-assisted medical triage and remote patient monitoring platform.',
                'mission': 'Expanding clinical capacity and improving patient outcomes worldwide.',
                'benefits': ['Wellness stipend', 'Flexible remote work', 'Mental health therapy coverage'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'TerraSphere Geomatics',
                'industry': 'GIS & Climate Tech',
                'size': '11-50',
                'founded': 2022,
                'headquarters': 'Vancouver, Canada',
                'website': 'https://terrasphere.example.com',
                'about': 'High-resolution satellite analytics for wildfire tracking, deforestation monitoring, and carbon credits.',
                'mission': 'Providing transparent planetary intelligence to protect biodiversity.',
                'benefits': ['Outdoor gear allowance', 'Flexible hours', 'Health spending account'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1524661135-423995f22d0b?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Synapse Media Streaming',
                'industry': 'Digital Media & Entertainment',
                'size': '501-1000',
                'founded': 2016,
                'headquarters': 'Los Angeles, CA',
                'website': 'https://synapsemedia.example.com',
                'about': 'Ultra-low latency live video streaming platform powering global gaming tournaments and creator broadcasts.',
                'mission': 'Bringing interactive entertainment to hundreds of millions in real-time.',
                'benefits': ['Streaming subscription credits', 'Generous 401(k)', 'Comprehensive Medical/Vision/Dental'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Vanguard Logistics Tech',
                'industry': 'Supply Chain & Logistics',
                'size': '1000+',
                'founded': 2013,
                'headquarters': 'Atlanta, GA',
                'website': 'https://vanguardlogistics.example.com',
                'about': 'End-to-end freight visibility and automated route optimization software.',
                'mission': 'Modernizing global freight transportation with intelligent logistics software.',
                'benefits': ['Annual bonus plan', 'Health savings account', 'Professional development grant'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Omicron Games Studio',
                'industry': 'Gaming & Interactive Entertainment',
                'size': '51-200',
                'founded': 2019,
                'headquarters': 'Montreal, Canada',
                'website': 'https://omicrongames.example.com',
                'about': 'Creators of critically acclaimed multiplayer action RPGs and Unreal Engine 5 virtual worlds.',
                'mission': 'Building unforgettable worlds that forge genuine social bonds.',
                'benefits': ['Free video games allowance', 'No crunch culture policy', 'Ergonomic home setup'],
                'is_verified': True,
                'is_featured': True,
                'logo_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Nexus Education Labs',
                'industry': 'EdTech & Learning',
                'size': '51-200',
                'founded': 2020,
                'headquarters': 'Dhaka / Singapore (Remote)',
                'website': 'https://nexusedu.example.com',
                'about': 'Adaptive STEM learning platforms and AI tutors personalized for K-12 students.',
                'mission': 'Democratizing world-class education for every child on Earth.',
                'benefits': ['Flexible working hours', 'Unlimited books/courses allowance', 'Annual company retreat'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Boreal Capital Management',
                'industry': 'Investment & Wealth Tech',
                'size': '51-200',
                'founded': 2017,
                'headquarters': 'Zurich, Switzerland',
                'website': 'https://borealcap.example.com',
                'about': 'Quantitative asset management and institutional portfolio risk modeling platform.',
                'mission': 'Generating alpha through systematic quantitative algorithmic research.',
                'benefits': ['Performance profit sharing', 'Swiss pension contributions', 'Top-tier private medical'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Cortex BioSensors',
                'industry': 'Wearable Health & IoT',
                'size': '11-50',
                'founded': 2023,
                'headquarters': 'Cambridge, UK',
                'website': 'https://cortexbiosensors.example.com',
                'about': 'Continuous non-invasive biochemical monitoring sensors and companion health AI apps.',
                'mission': 'Empowering preventative health through continuous molecular insights.',
                'benefits': ['Early employee equity', 'Comprehensive health insurance', 'Modern lab environment'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1507668077129-56e32842fceb?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Prism Creative Agency',
                'industry': 'Digital Marketing & Branding',
                'size': '11-50',
                'founded': 2021,
                'headquarters': 'Tokyo, Japan (Hybrid)',
                'website': 'https://prismagency.example.com',
                'about': 'High-end 3D motion design, viral brand campaigns, and creative tech installations.',
                'mission': 'Creating breathtaking brand moments that capture global attention.',
                'benefits': ['Creative gear budget', 'Flexible vacation', 'Modern studio in Shibuya'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1542744094-3a31f272c490?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1200&auto=format&fit=crop&q=80',
            },
            {
                'name': 'Horizon Space Systems',
                'industry': 'NewSpace & Propulsion',
                'size': '51-200',
                'founded': 2020,
                'headquarters': 'Huntsville, AL',
                'website': 'https://horizonspacesystems.example.com',
                'about': 'Reusable orbital transfer vehicles and cryogenic propulsion engines for satellite deployment.',
                'mission': 'Opening orbital transportation routes for the commercial space economy.',
                'benefits': ['Space launch watch events', '401(k) match', 'Comprehensive medical'],
                'is_verified': True,
                'is_featured': False,
                'logo_url': 'https://images.unsplash.com/photo-1517976487507-5b3a4a159981?w=200&auto=format&fit=crop&q=80',
                'cover_url': 'https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=1200&auto=format&fit=crop&q=80',
            },
        ]

        created_companies = []
        for cdata in companies_seed:
            comp, _ = Company.objects.get_or_create(
                name=cdata['name'],
                defaults={
                    'industry': cdata['industry'],
                    'company_size': cdata['size'],
                    'founded_year': cdata['founded'],
                    'headquarters': cdata['headquarters'],
                    'website': cdata['website'],
                    'about': cdata['about'],
                    'mission': cdata['mission'],
                    'benefits': cdata['benefits'],
                    'is_verified': cdata['is_verified'],
                    'verification_status': Company.VerificationStatus.VERIFIED if cdata['is_verified'] else Company.VerificationStatus.PENDING,
                    'is_featured': cdata['is_featured'],
                    'logo_url': cdata['logo_url'],
                    'cover_image_url': cdata['cover_url'],
                }
            )
            created_companies.append(comp)

        # 6. Create Primary Demo Employer: Sarah Jenkins @ Apex Global Technologies
        primary_company = created_companies[0]
        employer_user, _ = User.objects.get_or_create(
            email='employer@hiresphere.io',
            defaults={
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'role': User.Role.EMPLOYER,
                'phone': '+1 (415) 890-3421',
                'is_email_verified': True,
                'bio': 'VP of Global Talent Acquisition @ Apex Global Technologies. Passionate about hiring top engineers and fostering inclusive cultures.',
                'avatar_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80',
            }
        )
        employer_user.set_password('demo123456')
        employer_user.save()

        EmployerProfile.objects.get_or_create(
            user=employer_user,
            defaults={
                'company': primary_company,
                'designation': 'VP of Global Talent Acquisition',
                'department': 'Talent Operations',
                'is_primary': True
            }
        )

        # 7. Create Primary Demo Candidate: Alex Mercer
        candidate_user, _ = User.objects.get_or_create(
            email='candidate@hiresphere.io',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Mercer',
                'role': User.Role.CANDIDATE,
                'phone': '+1 (650) 430-8812',
                'is_email_verified': True,
                'bio': 'Senior Full Stack & Distributed Systems Engineer with 6+ years of production experience scaling React, Django, Go, and cloud architectures. Passionate about performant user interfaces and resilient microservices.',
                'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80',
            }
        )
        candidate_user.set_password('demo123456')
        candidate_user.save()

        cand_profile, _ = CandidateProfile.objects.get_or_create(
            user=candidate_user,
            defaults={
                'headline': 'Senior Full Stack Engineer (React, Python, Cloud)',
                'experience_years': 6,
                'preferred_location': 'San Francisco, CA / Remote',
                'preferred_employment_type': 'full_time',
                'expected_salary': 165000.00,
                'salary_currency': 'USD',
                'portfolio_url': 'https://alexmercer.dev',
                'github_url': 'https://github.com/alexmercer-dev',
                'linkedin_url': 'https://linkedin.com/in/alex-mercer-tech',
                'is_open_to_work': True,
                'profile_strength': 95,
            }
        )

        # Candidate Educations
        Education.objects.get_or_create(
            candidate=cand_profile,
            institution='University of California, Berkeley',
            degree='Bachelor of Science (B.S.)',
            field_of_study='Computer Science & Electrical Engineering',
            defaults={
                'start_date': '2016-09-01',
                'end_date': '2020-05-15',
                'grade': '3.88 GPA',
                'description': 'Coursework: Distributed Systems, Algorithms, Database Internals, Machine Learning, Operating Systems.'
            }
        )

        # Candidate Experiences
        Experience.objects.get_or_create(
            candidate=cand_profile,
            company_name='Vanguard Cloud Platform',
            job_title='Senior Software Engineer',
            defaults={
                'location': 'San Francisco, CA',
                'workplace_type': 'hybrid',
                'start_date': '2022-06-01',
                'is_current': True,
                'responsibilities': [
                    'Architected real-time microservices handling over 45,000 requests/sec with 99.99% availability using Go and Django.',
                    'Led frontend migration to React 18 and Tailwind CSS, improving Core Web Vitals and lowering page load times by 42%.',
                    'Mentored 5 junior engineers, led architectural design reviews, and established automated CI/CD deployment pipelines.'
                ],
                'description': 'Core contributor to flagship cloud orchestration suite and distributed telemetry engine.'
            }
        )

        Experience.objects.get_or_create(
            candidate=cand_profile,
            company_name='Nexus Stream Software',
            job_title='Full Stack Developer',
            defaults={
                'location': 'San Jose, CA',
                'workplace_type': 'remote',
                'start_date': '2020-06-01',
                'end_date': '2022-05-30',
                'is_current': False,
                'responsibilities': [
                    'Built scalable RESTful and GraphQL APIs in Python/Django backed by PostgreSQL and Redis caching.',
                    'Engineered reusable component library in React/TypeScript adopted across 4 internal engineering teams.',
                    'Optimized SQL query latency by 60% through indexed views and query plan refactoring.'
                ],
                'description': 'Developed customer-facing analytics dashboards and payment integration workflows.'
            }
        )

        # Candidate Skills
        candidate_skill_names = ['Python', 'Django', 'React.js', 'TypeScript', 'Docker', 'PostgreSQL', 'AWS', 'Kubernetes', 'Tailwind CSS']
        for sk_n in candidate_skill_names:
            if sk_n in skill_objs:
                CandidateSkill.objects.get_or_create(
                    candidate=cand_profile,
                    skill=skill_objs[sk_n],
                    defaults={'proficiency': CandidateSkill.ProficiencyLevel.EXPERT, 'years_of_experience': 5}
                )

        # Candidate Projects
        Project.objects.get_or_create(
            candidate=cand_profile,
            title='Distributed Task Pipeline & Real-Time Event Engine',
            defaults={
                'description': 'High-throughput async event processor with distributed locks, dead letter queues, and WebSocket telemetry.',
                'technologies': ['Python', 'Redis', 'Docker', 'React', 'FastAPI'],
                'project_url': 'https://github.com/alexmercer-dev/event-engine',
                'repository_url': 'https://github.com/alexmercer-dev/event-engine'
            }
        )

        # Candidate Certifications
        Certification.objects.get_or_create(
            candidate=cand_profile,
            name='AWS Certified Solutions Architect - Professional',
            defaults={
                'issuing_organization': 'Amazon Web Services',
                'issue_date': '2023-04-10',
                'credential_id': 'AWS-PSA-8829471'
            }
        )

        # Candidate Resume
        Resume.objects.get_or_create(
            candidate=cand_profile,
            title='Alex_Mercer_Senior_FullStack_Resume.pdf',
            defaults={
                'file_url': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
                'is_default': True,
                'file_size_kb': 284,
                'file_extension': 'pdf'
            }
        )

        # 8. Create additional candidate profiles for realistic ATS Kanban pipeline
        extra_candidates = [
            {'email': 'elena.rostova@example.com', 'name': ('Elena', 'Rostova'), 'title': 'Lead AI Research Engineer', 'exp': 7, 'salary': 190000, 'avatar': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&auto=format&fit=crop&q=80', 'skills': ['Python', 'PyTorch', 'Large Language Models (LLMs)', 'Docker', 'AWS']},
            {'email': 'marcus.chen@example.com', 'name': ('Marcus', 'Chen'), 'title': 'Senior DevOps & SRE Specialist', 'exp': 5, 'salary': 155000, 'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80', 'skills': ['Kubernetes', 'Docker', 'AWS', 'Terraform', 'CI/CD Pipelines']},
            {'email': 'sophia.martinez@example.com', 'name': ('Sophia', 'Martinez'), 'title': 'Principal Product Designer', 'exp': 8, 'salary': 160000, 'avatar': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&auto=format&fit=crop&q=80', 'skills': ['Figma', 'UI/UX Design', 'Design Systems', 'User Research']},
            {'email': 'david.kim@example.com', 'name': ('David', 'Kim'), 'title': 'Backend Systems Engineer (Go & Python)', 'exp': 4, 'salary': 145000, 'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&auto=format&fit=crop&q=80', 'skills': ['Go / Golang', 'Python', 'PostgreSQL', 'Docker', 'Django']},
            {'email': 'priya.patel@example.com', 'name': ('Priya', 'Patel'), 'title': 'Frontend Architect (React & Next.js)', 'exp': 6, 'salary': 150000, 'avatar': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=200&auto=format&fit=crop&q=80', 'skills': ['React.js', 'TypeScript', 'Next.js', 'Tailwind CSS']},
            {'email': 'jamal.washington@example.com', 'name': ('Jamal', 'Washington'), 'title': 'Cybersecurity Penetration Tester', 'exp': 5, 'salary': 140000, 'avatar': 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=200&auto=format&fit=crop&q=80', 'skills': ['Penetration Testing', 'Zero Trust Architecture', 'Python']},
            {'email': 'claire.dubois@example.com', 'name': ('Claire', 'Dubois'), 'title': 'Data Scientist & ML Engineer', 'exp': 3, 'salary': 130000, 'avatar': 'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?w=200&auto=format&fit=crop&q=80', 'skills': ['Python', 'Machine Learning', 'Data Analysis', 'Pandas & NumPy']},
            {'email': 'tariq.almansoor@example.com', 'name': ('Tariq', 'Al-Mansoor'), 'title': 'Full Stack Web Developer', 'exp': 2, 'salary': 115000, 'avatar': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200&auto=format&fit=crop&q=80', 'skills': ['React.js', 'Node.js', 'PostgreSQL', 'Tailwind CSS']},
        ]

        extra_candidate_profiles = []
        for cand_info in extra_candidates:
            u, _ = User.objects.get_or_create(
                email=cand_info['email'],
                defaults={
                    'first_name': cand_info['name'][0],
                    'last_name': cand_info['name'][1],
                    'role': User.Role.CANDIDATE,
                    'is_email_verified': True,
                    'avatar_url': cand_info['avatar'],
                    'bio': f"Experienced professional specialized in {cand_info['title']}."
                }
            )
            u.set_password('demo123456')
            u.save()

            cp, _ = CandidateProfile.objects.get_or_create(
                user=u,
                defaults={
                    'headline': cand_info['title'],
                    'experience_years': cand_info['exp'],
                    'preferred_location': 'Remote',
                    'preferred_employment_type': 'full_time',
                    'expected_salary': cand_info['salary'],
                    'profile_strength': random.randint(75, 95)
                }
            )
            # Add skills
            for s_item in cand_info['skills']:
                if s_item in skill_objs:
                    CandidateSkill.objects.get_or_create(
                        candidate=cp,
                        skill=skill_objs[s_item],
                        defaults={'proficiency': CandidateSkill.ProficiencyLevel.ADVANCED, 'years_of_experience': cand_info['exp']}
                    )

            # Add resume
            Resume.objects.get_or_create(
                candidate=cp,
                title=f"{cand_info['name'][0]}_{cand_info['name'][1]}_CV.pdf",
                defaults={'file_url': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf', 'is_default': True, 'file_size_kb': 210}
            )
            extra_candidate_profiles.append(cp)

        # 9. Jobs Data Generation (100+ Jobs)
        job_templates = [
            # Software Engineering
            ('Senior Full Stack Engineer (Python & React)', 'Software Engineering', 'full_time', 'hybrid', 'San Francisco, CA', 150000, 195000, 'senior', ['Python', 'Django', 'React.js', 'PostgreSQL', 'Docker'], 5),
            ('Staff Distributed Systems Backend Engineer', 'Software Engineering', 'full_time', 'remote', 'Remote, US/Canada', 180000, 230000, 'lead', ['Go / Golang', 'Python', 'Kubernetes', 'PostgreSQL'], 2),
            ('Frontend Platform Engineer (React & TypeScript)', 'Software Engineering', 'full_time', 'remote', 'Remote, Global', 130000, 165000, 'mid', ['React.js', 'TypeScript', 'Next.js', 'Tailwind CSS'], 3),
            ('Lead Python / Django Architect', 'Software Engineering', 'full_time', 'on_site', 'New York, NY', 170000, 215000, 'lead', ['Python', 'Django', 'PostgreSQL', 'AWS'], 1),
            ('Junior Full Stack Web Developer', 'Software Engineering', 'full_time', 'hybrid', 'Austin, TX', 85000, 110000, 'junior', ['React.js', 'Node.js', 'TypeScript', 'PostgreSQL'], 4),
            ('Engineering Manager - Core Platform', 'Software Engineering', 'full_time', 'hybrid', 'Seattle, WA', 195000, 250000, 'lead', ['Python', 'AWS', 'Agile / Scrum', 'Docker'], 1),
            ('Mobile Application Engineer (React Native)', 'Software Engineering', 'full_time', 'remote', 'Remote', 125000, 160000, 'mid', ['React.js', 'TypeScript', 'GraphQL'], 2),
            ('Embedded Firmware Engineer', 'Hardware & Embedded', 'full_time', 'on_site', 'Boston, MA', 135000, 175000, 'mid', ['Python', 'Docker'], 2),

            # Data Science & AI
            ('Senior Machine Learning Research Scientist', 'Data Science & AI', 'full_time', 'hybrid', 'San Francisco, CA', 185000, 245000, 'senior', ['Python', 'PyTorch', 'Large Language Models (LLMs)', 'Machine Learning'], 2),
            ('Generative AI Applications Engineer', 'Data Science & AI', 'full_time', 'remote', 'Remote', 160000, 210000, 'mid', ['Python', 'Large Language Models (LLMs)', 'React.js', 'FastAPI'], 3),
            ('Senior Data Engineer (Distributed Pipelines)', 'Data Science & AI', 'full_time', 'remote', 'Remote, US', 145000, 185000, 'senior', ['Python', 'PostgreSQL', 'AWS', 'Data Analysis'], 2),
            ('AI Safety & Red Teaming Specialist', 'Data Science & AI', 'full_time', 'hybrid', 'Boston, MA', 155000, 195000, 'mid', ['Python', 'Large Language Models (LLMs)', 'Cybersecurity'], 1),
            ('Computer Vision Engineer', 'Data Science & AI', 'full_time', 'on_site', 'San Diego, CA', 140000, 180000, 'mid', ['Python', 'PyTorch', 'Docker'], 2),
            ('Lead Quantitative Data Scientist', 'Data Science & AI', 'full_time', 'hybrid', 'New York, NY', 190000, 260000, 'lead', ['Python', 'Data Analysis', 'Pandas & NumPy'], 1),

            # DevOps & Cloud
            ('Senior Cloud Security & SRE Engineer', 'DevOps & Cloud', 'full_time', 'remote', 'Remote', 160000, 205000, 'senior', ['Kubernetes', 'Docker', 'AWS', 'Terraform', 'CI/CD Pipelines'], 3),
            ('Principal Kubernetes Infrastructure Architect', 'DevOps & Cloud', 'full_time', 'remote', 'Remote, Global', 185000, 235000, 'lead', ['Kubernetes', 'Terraform', 'AWS', 'Docker'], 2),
            ('DevOps Automation Engineer', 'DevOps & Cloud', 'full_time', 'hybrid', 'Austin, TX', 125000, 160000, 'mid', ['Docker', 'CI/CD Pipelines', 'AWS', 'Python'], 4),
            ('Cloud Platform Architect (Multi-Cloud GCP/AWS)', 'DevOps & Cloud', 'full_time', 'hybrid', 'Seattle, WA', 175000, 220000, 'senior', ['AWS', 'GCP', 'Terraform', 'Kubernetes'], 2),

            # Product & Design
            ('Lead Product Designer (Design Systems & Web)', 'Product & Design', 'full_time', 'remote', 'Remote', 140000, 180000, 'senior', ['Figma', 'UI/UX Design', 'Design Systems', 'User Research'], 2),
            ('Senior Technical Product Manager (Cloud Platform)', 'Product & Design', 'full_time', 'hybrid', 'San Francisco, CA', 165000, 215000, 'senior', ['Product Strategy', 'Agile / Scrum', 'AWS'], 2),
            ('Product Designer - Enterprise SaaS', 'Product & Design', 'full_time', 'remote', 'Remote', 115000, 150000, 'mid', ['Figma', 'UI/UX Design', 'Design Systems'], 3),
            ('Director of Product Management', 'Product & Design', 'full_time', 'hybrid', 'New York, NY', 210000, 275000, 'executive', ['Product Strategy', 'Agile / Scrum'], 1),

            # Cybersecurity
            ('Senior Cloud Penetration Tester & Ethical Hacker', 'Cybersecurity', 'full_time', 'remote', 'Remote', 150000, 190000, 'senior', ['Penetration Testing', 'Zero Trust Architecture', 'Python'], 2),
            ('Security Operations Center (SOC) Lead', 'Cybersecurity', 'full_time', 'on_site', 'Austin, TX', 135000, 175000, 'senior', ['SOC Analysis', 'Cybersecurity'], 2),
            ('Application Security Engineer (AppSec)', 'Cybersecurity', 'full_time', 'remote', 'Remote', 140000, 185000, 'mid', ['Python', 'Docker', 'Penetration Testing'], 2),

            # Marketing & Sales
            ('Director of Developer Relations (DevRel)', 'Marketing & Growth', 'full_time', 'remote', 'Remote', 150000, 195000, 'senior', ['Python', 'React.js', 'Product Strategy'], 1),
            ('Technical Enterprise Account Executive', 'Sales & Customer Success', 'full_time', 'hybrid', 'San Francisco, CA', 120000, 240000, 'senior', ['Product Strategy', 'Agile / Scrum'], 3),
            ('Product Marketing Manager - AI & Cloud', 'Marketing & Growth', 'full_time', 'remote', 'Remote', 130000, 170000, 'mid', ['Product Strategy', 'Figma'], 2),
        ]

        responsibilities_pool = [
            "Architect, build, and maintain mission-critical production services with high uptime.",
            "Collaborate closely with cross-functional product, design, and infrastructure teams.",
            "Write modular, tested, and thoroughly documented code following modern engineering standards.",
            "Participate in constructive code reviews, technical architecture debates, and post-mortems.",
            "Diagnose, profile, and optimize performance bottlenecks in database queries and API pipelines.",
            "Drive CI/CD automation, unit testing coverage, and deployment safety mechanisms."
        ]

        requirements_pool = [
            "Demonstrated experience building high-scale distributed systems in production.",
            "Deep proficiency with modern web architectures, API design principles, and relational databases.",
            "Strong communication skills and empathy in asynchronous, distributed team environments.",
            "Proficiency with containerization (Docker) and cloud deployments (AWS / GCP).",
            "Bachelor's degree in Computer Science or equivalent practical industry experience."
        ]

        benefits_pool = [
            "Comprehensive Medical, Vision, and Dental insurance (100% covered for employee)",
            "401(k) retirement plan with 5% immediate company match",
            "Generous equipment allowance for ergonomic home office setup",
            "Unlimited paid time off (PTO) with minimum 3-week recommended threshold",
            "Annual $2,500 continuous learning, conferences, and certifications stipend"
        ]

        created_jobs = []
        now = timezone.now()

        # Generate ~110 jobs across companies and variations
        job_count = 0
        for comp in created_companies:
            # 5-6 jobs per company
            num_jobs_for_company = 5 if comp == primary_company else random.randint(4, 6)
            
            for _ in range(num_jobs_for_company):
                tmpl = random.choice(job_templates)
                cat_obj = category_objs.get(tmpl[1], category_objs['Software Engineering'])
                
                # Vary title slightly for realism
                title = tmpl[0]
                if comp != primary_company and random.random() > 0.6:
                    prefixes = ['Senior', 'Staff', 'Lead', 'Principal', 'Core', 'Global']
                    prefix = random.choice(prefixes)
                    if not title.startswith(prefix):
                        title = f"{prefix} {title}"

                # Post date in the past 1-25 days
                days_ago = random.randint(1, 25)
                posted_time = now - timedelta(days=days_ago)
                deadline_time = posted_time + timedelta(days=random.randint(15, 45))

                job = Job.objects.create(
                    company=comp,
                    posted_by=employer_user if comp == primary_company else admin_user,
                    title=title,
                    department=tmpl[1].split('&')[0].strip(),
                    category=cat_obj,
                    employment_type=tmpl[2],
                    workplace_type=tmpl[3],
                    location=tmpl[4] if tmpl[3] != 'remote' else 'Remote (Anywhere)',
                    min_salary=tmpl[5],
                    max_salary=tmpl[6],
                    salary_currency='USD',
                    is_salary_negotiable=random.choice([True, False]),
                    experience_level=tmpl[7],
                    description=f"We are looking for a talented and driven **{title}** to join the engineering organization at **{comp.name}**.\n\nYou will work on high-impact projects that directly affect our customers and platform reliability.",
                    responsibilities=responsibilities_pool[:random.randint(4, 6)],
                    requirements=requirements_pool[:random.randint(3, 5)],
                    benefits=comp.benefits or benefits_pool[:4],
                    vacancies=tmpl[9],
                    deadline=deadline_time,
                    status=Job.Status.PUBLISHED,
                    is_featured=(comp.is_featured and random.random() > 0.5),
                    views_count=random.randint(45, 1280),
                )
                job.created_at = posted_time
                job.save()

                # Add skills
                for sk_name in tmpl[8]:
                    if sk_name in skill_objs:
                        JobSkill.objects.get_or_create(job=job, skill=skill_objs[sk_name], defaults={'is_required': True})

                created_jobs.append(job)
                job_count += 1

        self.stdout.write(self.style.SUCCESS(f"[OK] Generated {job_count} jobs across {len(created_companies)} companies."))

        # 10. Populate ATS pipeline for Primary Employer's Jobs (Apex Global Technologies)
        apex_jobs = [j for j in created_jobs if j.company == primary_company]
        main_job = apex_jobs[0] if apex_jobs else created_jobs[0]

        all_cands = [cand_profile] + extra_candidate_profiles
        statuses_pipeline = [
            (all_cands[0], JobApplication.Status.INTERVIEW, "Exceptional technical profile and distributed systems background. Candidate performed strongly in initial phone screen."),
            (all_cands[1], JobApplication.Status.OFFER, "Candidate passed all 4 rounds with flying colors. Written offer package sent."),
            (all_cands[2], JobApplication.Status.SHORTLISTED, "Strong Kubernetes & Terraform experience matching infrastructure needs."),
            (all_cands[3], JobApplication.Status.SCREENING, "Portfolio under review by design lead."),
            (all_cands[4], JobApplication.Status.APPLIED, "New candidate submission."),
            (all_cands[5], JobApplication.Status.HIRED, "Offer accepted! Onboarding starts next month."),
            (all_cands[6], JobApplication.Status.ASSESSMENT, "Take-home practical security exercise sent."),
            (all_cands[7], JobApplication.Status.REJECTED, "Seeking more senior candidate with 5+ years experience."),
        ]

        for cand, app_st, note_txt in statuses_pipeline:
            app, _ = JobApplication.objects.get_or_create(
                job=main_job,
                candidate=cand,
                defaults={
                    'resume': cand.resumes.first(),
                    'cover_letter': f"Dear Hiring Team at {main_job.company.name},\n\nI am thrilled to apply for the {main_job.title} position. With my extensive background in modern software engineering, I am confident in delivering rapid value to your team.",
                    'expected_salary': cand.expected_salary or 150000,
                    'status': app_st,
                    'availability_notice': '2 weeks notice',
                }
            )
            app.calculate_match_score()

            ApplicationStatusHistory.objects.get_or_create(
                application=app,
                from_status='applied',
                to_status=app_st,
                defaults={'note': note_txt, 'changed_by': employer_user}
            )

            if note_txt:
                RecruiterNote.objects.get_or_create(
                    application=app,
                    author=employer_user,
                    defaults={'note': note_txt, 'is_private': True}
                )

        # 11. Schedule Interviews
        Interview.objects.get_or_create(
            application=JobApplication.objects.filter(job=main_job, candidate=cand_profile).first(),
            interviewer=employer_user,
            defaults={
                'title': 'Technical Systems & Architecture Deep-Dive',
                'interview_type': Interview.InterviewType.ONLINE,
                'scheduled_at': timezone.now() + timedelta(days=2, hours=4),
                'duration_minutes': 60,
                'meeting_link': 'https://meet.google.com/hsp-tech-apex',
                'instructions': 'Please be prepared to discuss distributed systems tradeoffs, database indexing, and your recent production projects.',
                'status': Interview.Status.SCHEDULED
            }
        )

        # 12. Candidate Applications across other companies
        for extra_j in created_jobs[5:10]:
            app, _ = JobApplication.objects.get_or_create(
                job=extra_j,
                candidate=cand_profile,
                defaults={
                    'resume': cand_profile.resumes.first(),
                    'cover_letter': f"Excited about the mission at {extra_j.company.name}. Looking forward to connecting!",
                    'expected_salary': 160000,
                    'status': random.choice([JobApplication.Status.APPLIED, JobApplication.Status.SCREENING, JobApplication.Status.SHORTLISTED]),
                }
            )
            app.calculate_match_score()

        # 13. Candidate Saved Jobs & Alerts
        for sj in created_jobs[12:16]:
            SavedJob.objects.get_or_create(candidate=cand_profile, job=sj)

        JobAlert.objects.get_or_create(
            candidate=cand_profile,
            title='Senior Full Stack & Python Jobs (Remote)',
            defaults={
                'keywords': 'Python React Senior Full Stack',
                'category': category_objs['Software Engineering'],
                'location': 'Remote',
                'employment_type': 'full_time',
                'frequency': JobAlert.Frequency.DAILY,
                'is_active': True
            }
        )

        # 14. Messaging Conversation
        conv, _ = Conversation.objects.get_or_create(
            job=main_job,
            employer=employer_user,
            candidate=candidate_user
        )
        Message.objects.get_or_create(
            conversation=conv,
            sender=employer_user,
            defaults={
                'content': f"Hi Alex! We were really impressed by your profile and distributed systems experience for the {main_job.title} role. We've scheduled a technical deep-dive for this Thursday. Let us know if the time works for you!"
            }
        )
        Message.objects.get_or_create(
            conversation=conv,
            sender=candidate_user,
            defaults={
                'content': "Hi Sarah, thank you so much! The time works perfectly for me. Looking forward to speaking with the team."
            }
        )

        # 15. Notifications for candidate and employer
        Notification.objects.get_or_create(
            recipient=candidate_user,
            title="Interview scheduled with Apex Global Technologies",
            defaults={
                'message': f"Your technical interview for '{main_job.title}' is scheduled for Thursday.",
                'notification_type': Notification.NotificationType.INTERVIEW_INVITE,
                'action_url': '/candidate/interviews',
                'is_read': False
            }
        )
        Notification.objects.get_or_create(
            recipient=employer_user,
            title="New application received",
            defaults={
                'message': f"Alex Mercer applied for '{main_job.title}' with a 94% profile match score.",
                'notification_type': Notification.NotificationType.NEW_APPLICATION,
                'action_url': '/employer/ats',
                'is_read': False
            }
        )

        # 16. Reported Job for Admin Moderation
        scam_job = created_jobs[-1]
        JobReport.objects.get_or_create(
            job=scam_job,
            reporter=candidate_user,
            defaults={
                'reason': JobReport.Reason.MISLEADING_SALARY,
                'details': 'The salary range listed in description does not match initial conversation.',
                'status': JobReport.Status.PENDING
            }
        )

        self.stdout.write(self.style.SUCCESS("[SUCCESS] Database seeding completed successfully!"))
        self.stdout.write(self.style.SUCCESS("Credentials:\n- Candidate: candidate@hiresphere.io / demo123456\n- Employer: employer@hiresphere.io / demo123456\n- Admin: admin@hiresphere.io / demo123456"))
