
# IntelliFlow – Intelligent Workflow and Project Management System

IntelliFlow is a web-based task and workflow management application built using Python and Flask. It helps users organize tasks, manage deadlines, track productivity, and monitor their work through an interactive dashboard.

## Features

- User Registration and Login
- Secure Password Hashing
- Personalized User Dashboard
- Add, Edit, Complete and Delete Tasks
- Automatic Task Priority Assignment
- Task Deadline Management
- Overdue Task Alerts
- Search Tasks by Title and Description
- Filter Tasks by Status and Priority
- Productivity Analytics Dashboard
- Dynamic Productivity Progress Bar
- SQLite Database Integration

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| Flask-SQLAlchemy | Database integration |
| SQLite | Data storage |
| HTML5 | Frontend structure |
| CSS3 | User interface styling |
| JavaScript | Search and filtering |
| Chart.js | Productivity analytics |
| Flask-Login | User authentication |

## Project Structure

```text
IntelliFlow/
│
├── app.py
├── requirements.txt
├── README.md
│
├── instance/
│   └── intelliflow.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── edit_task.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd IntelliFlow
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open your browser:

http://127.0.0.1:5000

## Automatic Priority System

IntelliFlow assigns task priorities based on keywords and deadlines.

- High: Urgent keywords or deadlines within one day.
- Medium: Relevant project keywords or deadlines within three days.
- Low: Other tasks without an urgent deadline.

## Productivity Calculation

Productivity is calculated using:

Productivity (%) = (Completed Tasks / Total Tasks) × 100

## Future Enhancements

- Email Notifications
- Calendar Integration
- Advanced Analytics
- Team Collaboration
- AI-Based Task Recommendations

## Author

Developed as a software development portfolio project.
