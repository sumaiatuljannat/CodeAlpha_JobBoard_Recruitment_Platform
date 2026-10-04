# 💼 Job Board & Recruitment Platform

🌐 **Live Application**  
👉 [Visit the Live Job Board](https://codealpha-jobboard-recruitment-platform-2.onrender.com/)

📦 **GitHub Repository**  
👉 [View Source Code on GitHub](https://github.com/sumaiatuljannat/CodeAlpha_JobBoard_Recruitment_Platform)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![Django REST Framework](https://img.shields.io/badge/DRF-REST-red?logo=django)
![React](https://img.shields.io/badge/React-19.x-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-8.x-646CFF?logo=vite)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-06B6D4?logo=tailwindcss)
![Axios](https://img.shields.io/badge/Axios-HTTP_Client-5A29E4)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?logo=render)

---

## 📌 Overview

A modern, full-stack **Job Board & Recruitment Management Platform** designed to connect job seekers with recruiters through a centralized hiring workflow.

The platform allows **candidates to discover jobs, create profiles, upload resumes, and submit applications**, while **recruiters can manage companies, publish job vacancies, review candidates, and manage recruitment activities**.

The application follows a modern client-server architecture with a **React frontend**, **Django REST API backend**, and **PostgreSQL database**, and is deployed as a publicly accessible web application.

---

## 🌐 Live Application

### 🚀 Try the Platform

👉 **[Open Job Board — Live](https://codealpha-jobboard-recruitment-platform-2.onrender.com/)**

The deployed application is publicly accessible through Render.

### 🔗 Deployment Architecture

| Component | Technology | Deployment |
|---|---|---|
| Frontend | React + Vite | Render Static Site |
| Backend | Django + Django REST Framework | Render Web Service |
| Database | PostgreSQL | Render PostgreSQL |
| API Communication | Axios / REST API | HTTPS |
| Source Code | Git + GitHub | GitHub |

---

# 🌟 Key Features

## 👤 Candidate Features

### 🔎 Job Discovery

Candidates can:

- Browse available job opportunities
- Search for relevant positions
- Explore job details
- Review company information
- View job requirements and descriptions
- Find suitable opportunities based on their interests

### 👤 Candidate Profile

Candidates can create and manage their professional profile including:

- Personal information
- Professional summary
- Skills
- Education
- Experience
- Resume
- Professional details

### 📄 Resume Management

The platform supports resume-related workflows so candidates can maintain their professional information and use their profile while applying for jobs.

### 📝 Job Applications

Candidates can:

- Apply for available jobs
- Submit applications
- Track application information
- View application status
- Manage their recruitment activity

### 🔐 Authentication

Candidate accounts are protected through authenticated API access and JWT-based authentication.

---

# 🏢 Recruiter Features

## 📢 Job Posting

Recruiters can create and publish job vacancies containing information such as:

- Job title
- Company
- Description
- Requirements
- Skills
- Location
- Employment information
- Compensation-related information where applicable

Published jobs become available for candidates to discover and apply for.

## 👥 Candidate Management

Recruiters can manage candidate applications and review applicants associated with their job postings.

Recruitment workflows can be used to organize candidates throughout the hiring process.

## 📊 Recruitment Management

The platform is designed around a centralized recruitment workflow, allowing recruiters to manage:

- Job postings
- Applications
- Candidates
- Recruitment progress
- Interview-related activities
- Notifications

---

# 📅 Interview Management

The platform includes interview-related functionality for organizing recruitment activities.

Recruitment teams can manage interview information and coordinate interview stages as part of the hiring workflow.

---

# 💬 Messaging

The platform includes messaging functionality to support communication between users within the recruitment workflow.

This provides a centralized communication layer instead of relying entirely on external communication tools.

---

# 🔔 Notifications

Users can receive application and recruitment-related notifications through the platform.

The notification system helps users stay informed about important events in their recruitment workflow.

---

# 🎯 Job Recommendations

The platform includes job recommendation functionality designed to help candidates discover opportunities based on relevant profile information such as skills and location.

---

# 🛡️ Authentication & Authorization

The backend uses token-based authentication to protect API resources.

### Authentication Flow

```text
User
  │
  ├── Register
  │
  ├── Login
  │
  ▼
JWT Access Token
  │
  ▼
Authenticated API Requests
  │
  ├── Candidate Resources
  │
  └── Recruiter Resources
```

The frontend stores the authentication state and attaches the JWT access token to protected API requests.

The Axios client also handles token refresh when an access token expires.

---

# 🔐 Security

Security-related considerations implemented in the application include:

- JWT-based authentication
- Protected API endpoints
- Role-aware application workflows
- Authenticated job/application operations
- Backend validation
- Database-backed access control
- Private user-related resources
- Protected recruiter functionality
- Environment-based production configuration

Sensitive production configuration such as secret keys and database credentials should be supplied through environment variables rather than committed to Git.

---

# 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite |
| UI | Tailwind CSS, CSS |
| Icons | Lucide React |
| Routing | React Router |
| HTTP Client | Axios |
| Charts | Recharts |
| Backend | Python, Django |
| API | Django REST Framework |
| Authentication | JWT |
| Database | PostgreSQL |
| Development Database | SQLite fallback where configured |
| Production Server | Gunicorn |
| Deployment | Render |
| Version Control | Git & GitHub |

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       Users         │
                         │                     │
                         │ Candidates          │
                         │ Recruiters          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │                     │
                         │ React + Vite        │
                         │ Tailwind CSS        │
                         │ React Router        │
                         │ Axios               │
                         └──────────┬──────────┘
                                    │
                              REST API / HTTPS
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Django Backend    │
                         │                     │
                         │ Django              │
                         │ Django REST API     │
                         │ JWT Authentication  │
                         │ Business Logic      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    PostgreSQL       │
                         │                     │
                         │ Users               │
                         │ Companies           │
                         │ Jobs                │
                         │ Applications        │
                         │ Profiles            │
                         │ Notifications       │
                         │ Interviews          │
                         │ Messages            │
                         └─────────────────────┘
```

---

# 📁 Project Structure

```text
CodeAlpha_JobBoard_Recruitment_Platform/
│
├── backend/
│   │
│   ├── apps/
│   │   ├── authentication/
│   │   ├── profiles/
│   │   ├── companies/
│   │   ├── jobs/
│   │   ├── applications/
│   │   ├── notifications/
│   │   ├── interviews/
│   │   ├── messages/
│   │   └── ...
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── ...
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js
│   │   │
│   │   ├── assets/
│   │   │
│   │   ├── components/
│   │   │   └── common/
│   │   │
│   │   ├── context/
│   │   │
│   │   ├── pages/
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── .gitignore
└── README.md
```

---

# 🔄 Application Workflow

## Candidate Workflow

```text
Register
   ↓
Login
   ↓
Create / Complete Profile
   ↓
Upload Resume
   ↓
Browse Jobs
   ↓
View Job Details
   ↓
Apply
   ↓
Track Application
   ↓
Receive Notifications
   ↓
Interview / Recruitment Process
```

## Recruiter Workflow

```text
Register / Login
   ↓
Create Company Profile
   ↓
Create Job
   ↓
Publish Vacancy
   ↓
Receive Applications
   ↓
Review Candidates
   ↓
Manage Recruitment Pipeline
   ↓
Schedule Interviews
   ↓
Update Candidate Status
   ↓
Complete Hiring Process
```

---

# 🔌 API Architecture

The backend exposes RESTful API endpoints for the frontend application.

Example resource categories include:

```text
/api/
├── profiles/
├── companies/
├── jobs/
├── applications/
├── notifications/
├── interviews/
├── messages/
├── job-alerts/
└── audit-logs/
```

Protected endpoints require authenticated access using JWT tokens.

---

# ⚙️ Environment Variables

## Backend

Production configuration should be provided through environment variables.

Example:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=your-production-database-url
ALLOWED_HOSTS=your-render-hostname
```

> Never commit real production secrets, passwords, API keys, or database credentials to GitHub.

---

## Frontend

The frontend uses Vite environment variables for the backend API URL.

```env
VITE_API_URL=https://codealpha-jobboard-recruitment-platform-1.onrender.com
```

The frontend API client uses the configured API URL for production requests.

---

# 💻 Local Development Setup

## 1. Clone the Repository

```bash
git clone https://github.com/sumaiatuljannat/CodeAlpha_JobBoard_Recruitment_Platform.git
```

```bash
cd CodeAlpha_JobBoard_Recruitment_Platform
```

---

# 🐍 Backend Setup

## 2. Open Backend Directory

```bash
cd backend
```

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 4. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create a `.env` file according to the backend configuration used by the project.

Example:

```env
DEBUG=True
SECRET_KEY=your-development-secret-key
DATABASE_URL=your-database-url
```

---

## 6. Run Database Migrations

```bash
python manage.py migrate
```

---

## 7. Create an Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create the Django administrator account.

---

## 8. Start Backend Server

```bash
python manage.py runserver
```

Backend will normally be available at:

```text
http://127.0.0.1:8000
```

---

# ⚛️ Frontend Setup

Open a second terminal.

## 9. Enter Frontend Directory

From the project root:

```bash
cd frontend
```

## 10. Install Dependencies

```bash
npm install
```

---

## 11. Configure API URL

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## 12. Start React Development Server

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🏭 Production Build

To create a production frontend build:

```bash
npm run build
```

The generated production files are placed in:

```text
frontend/dist/
```

To preview the production build locally:

```bash
npm run preview
```

---

# 🚀 Production Deployment

The application is deployed using **Render** with separate frontend, backend, and database services.

## Frontend

```text
Platform: Render Static Site
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

## Backend

```text
Platform: Render Web Service
Root Directory: backend
Build Command:
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

Start Command:
gunicorn config.wsgi:application
```

## Database

```text
PostgreSQL
```

The frontend communicates with the deployed backend through:

```env
VITE_API_URL=https://codealpha-jobboard-recruitment-platform-1.onrender.com
```

---

# 🌐 Production URLs

### Frontend

👉 **[https://codealpha-jobboard-recruitment-platform-2.onrender.com/](https://codealpha-jobboard-recruitment-platform-2.onrender.com/)**

### Backend API Server

👉 **[https://codealpha-jobboard-recruitment-platform-1.onrender.com/](https://codealpha-jobboard-recruitment-platform-1.onrender.com/)**

> The backend root URL may return a `404 Not Found` response if no root route is defined. This does not mean the API server is offline; API functionality is exposed through its configured endpoints.

---

# 🧪 Testing Checklist

Before presenting the application, test the following workflows:

### Authentication

- [ ] Candidate registration
- [ ] Recruiter registration
- [ ] Login
- [ ] Logout
- [ ] JWT authentication
- [ ] Token refresh
- [ ] Protected routes

### Candidate

- [ ] Create profile
- [ ] Update profile
- [ ] Add skills
- [ ] Upload resume
- [ ] Browse jobs
- [ ] Search jobs
- [ ] View job details
- [ ] Apply for a job
- [ ] View applications
- [ ] Check notifications

### Recruiter

- [ ] Create company
- [ ] Create job
- [ ] Edit job
- [ ] Publish job
- [ ] View applications
- [ ] Review candidates
- [ ] Manage application status
- [ ] Schedule interview
- [ ] View recruitment activity

### Platform

- [ ] API connectivity
- [ ] Database operations
- [ ] Responsive UI
- [ ] Navigation
- [ ] Error handling
- [ ] Authentication persistence
- [ ] Production API URL
- [ ] Frontend deployment

---

# 📊 Main Modules

| Module | Purpose |
|---|---|
| Authentication | Registration, login and JWT authentication |
| Profiles | Candidate and recruiter profile management |
| Companies | Company information and recruiter management |
| Jobs | Job creation, publishing and discovery |
| Applications | Candidate job applications and tracking |
| Notifications | Recruitment-related notifications |
| Interviews | Interview scheduling and management |
| Messages | User-to-user recruitment communication |
| Job Alerts | Job opportunity notifications |
| Audit Logs | Administrative activity tracking |

---

# 🎨 Frontend

The frontend is built using a modern React-based architecture.

### Main Technologies

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- Lucide React
- Recharts

The frontend is responsible for:

- User interface
- Navigation
- Authentication state
- API communication
- Job discovery
- Profile management
- Application workflows
- Recruiter dashboards
- Recruitment interactions

---

# ⚙️ Backend

The backend is built with:

- Python
- Django
- Django REST Framework
- JWT authentication
- PostgreSQL

The backend handles:

- Authentication
- Authorization
- Business logic
- Database operations
- Job management
- Applications
- Profiles
- Recruitment workflows
- Notifications
- Interviews
- Messaging
- API endpoints

---

# 🗄️ Database

The production application uses **PostgreSQL** for persistent relational data.

The database stores information associated with the platform's major entities, including:

- Users
- Profiles
- Companies
- Jobs
- Applications
- Notifications
- Interviews
- Messages
- Job alerts
- Audit records

---

# 📱 Responsive Design

The frontend is designed to provide a responsive experience across:

- Desktop
- Laptop
- Tablet
- Mobile devices

The UI uses reusable React components and Tailwind CSS utilities to maintain a consistent design system.

---

# 🔒 Production Security Notes

For production deployments:

- Keep `SECRET_KEY` private.
- Never commit `.env` files containing secrets.
- Use HTTPS for production communication.
- Keep database credentials private.
- Restrict allowed hosts.
- Protect authenticated API endpoints.
- Validate user-provided data on the backend.
- Use proper access control for recruiter and candidate resources.

---

# 🚧 Future Improvements

Potential future improvements include:

- Advanced AI-powered job recommendations
- Resume parsing and skill extraction
- Automated candidate matching
- Email notification integration
- Cloud object storage for resumes
- Advanced recruiter analytics
- Interview video integration
- Real-time chat using WebSockets
- Advanced search and filtering
- Saved jobs
- Company reviews
- Application timeline visualization
- Multi-language support
- Automated deployment pipelines
- Comprehensive end-to-end testing

---

# 📸 Screenshots

Screenshots can be added here to demonstrate the major application interfaces.

Suggested screenshots:

```text
1. Home / Job Search
2. Login
3. Candidate Dashboard
4. Recruiter Dashboard
5. Job Details
6. Job Creation
7. Application Management
8. Candidate Profile
9. Resume Upload
10. Interview Management
```

Example:

```markdown
![Home Page](screenshots/home.png)
```

---

# 🎓 Project Purpose

This project was developed as a full-stack web application to demonstrate practical knowledge of:

- Full-stack development
- REST API development
- Database design
- Authentication
- Authorization
- Frontend development
- Backend development
- Recruitment workflow design
- API integration
- Deployment
- Git & GitHub
- Production-oriented application architecture

---

# 📚 Learning Outcomes

Through this project, the following development concepts were practiced:

- Building REST APIs with Django REST Framework
- Connecting React applications with backend APIs
- Implementing JWT authentication
- Designing relational database models
- Managing CRUD operations
- Handling user roles and permissions
- Building reusable React components
- Managing frontend state
- Implementing protected routes
- Deploying frontend and backend separately
- Connecting production services
- Working with PostgreSQL
- Using Git and GitHub for version control

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

### Basic workflow

```bash
git clone https://github.com/sumaiatuljannat/CodeAlpha_JobBoard_Recruitment_Platform.git
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Commit your changes:

```bash
git add .
git commit -m "Add your feature"
```

Push the branch:

```bash
git push origin feature/your-feature
```

Then open a Pull Request on GitHub.

---

# 📄 License

This project is available for educational and portfolio purposes.

---

# 👩‍💻 Author

**Sumaiatul Jannat**

Computer Science & Engineering Student

### 🔗 Project Links

🌐 **Live Application:**  
https://codealpha-jobboard-recruitment-platform-2.onrender.com/

💻 **GitHub Repository:**  
https://github.com/sumaiatuljannat/CodeAlpha_JobBoard_Recruitment_Platform

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

**Built with ❤️ using React, Django, Django REST Framework, PostgreSQL and modern web technologies.**
