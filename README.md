# Antigravity - Employee Management System (EMS)

A comprehensive, highly polished, and responsive **Employee Management System** built with **Django 5.x**, **SQLite3**, and **Bootstrap 5**. This application features an interactive dashboard with dynamic data visualization, soft deletion capability, robust validation, and user authentication, making it a state-of-the-art solution for student profiles or organizational management.

---

## 🌟 Key Features

### 🔐 User Authentication
- Secure login and logout using Django's built-in session-based authentication framework.
- Automatic redirection to the login page for unauthorized/guest users.
- Custom redirection handling upon login/logout with interactive status notifications.

### 📊 Interactive Dashboard
- **Analytics Cards**: Total registered employees, Active staff, and Inactive staff counts.
- **Charts Dashboard**:
  - Department distribution bar chart.
  - Active vs. Inactive employee ratio doughnut chart.
  - Gender distribution breakdown doughnut chart.
- **Recent Activities Feed**: Quick tracking of updated or newly created profiles.
- **Quick Navigation**: Standard navbar and responsive sidebar for streamlined portal navigation.

### 👔 Employee Directory (CRUD)
- **Grid Layout Table**: Profiles displayed in a Bootstrap table including profile images (with fallback defaults).
- **Interactive Sorting**: Instantly sort records alphabetically (Name), sequentially (Employee ID), or numerically (Salary, Date Joined).
- **Asynchronous Search**: Dynamic, page-reload-free search bar searching across multiple columns (Name, ID, Email, Phone, Department, City).
- **Multi-Filter Systems**: Filter profiles by Department, Designation, Status, or Gender simultaneously.
- **Pagination**: Neat paginated layout displaying 10 profiles per page.
- **Soft Deletion**: Employees deleted from directories are soft-deleted (`is_deleted=True`) to maintain historical database integrity.
- **Detail View Pages**: Profile summary with dedicated tabbed views (Personal Info, Job Specifics, Address & Contact).

### 🏢 Department & Designation Management
- Dedicated CRUD screens to manage company departments and job designations.
- Automatically calculates employee counters associated with departments and designations.

### 🛡️ Robust Validations
- **Frontend Real-time Checks**: Custom scripts validating email formats, phone numbers (exactly 10 digits), positive salaries, and joining dates (joining date cannot precede DOB, and age must be at least 18).
- **Backend Model Checks**: Full validator fields checking duplicate emails and numeric limits, returning structured feedback errors.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.14.0, Django 5.x
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla ES6)
- **Libraries & CDNs**:
  - Bootstrap 5 (CSS / JS bundle)
  - FontAwesome 6 (Icons)
  - Chart.js (Data charts)
- **Image Processing**: Pillow

---

## 📂 Project Structure

```text
employee_management/
│
├── manage.py
├── seed_data.py
│
├── employee_management/      # Main Project Configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── employees/                # Employee CRUD & Authentication
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── departments/              # Department Management App
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── admin.py
│
├── designations/             # Designation Management App
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── admin.py
│
├── templates/                # Global HTML Templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── 404.html
│   ├── employees/            # Employee views
│   ├── departments/          # Department views
│   └── designations/         # Designation views
│
└── static/                   # Global Assets
    ├── css/
    │   ├── style.css
    │   ├── dashboard.css
    │   ├── forms.css
    │   └── tables.css
    ├── js/
    │   ├── main.js
    │   ├── validation.js
    │   └── search.js
    └── images/
        ├── logo.png
        └── default-avatar.png
```

---

## 🚀 Installation & Setup Instructions

To run this project locally, follow these steps:

### 1. Clone the repository and navigate to root directory
```bash
cd Mini
```

### 2. Initialize and Activate Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / MacOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Database Schemas & Run Migrations
```bash
cd employee_management
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Database (Creates Admin Account & Sample Data)
```bash
python seed_data.py
```
*Note: Running this command creates the administrative credentials and populates the database with 5 departments, 7 designations, and 12 sample employees.*

### 6. Start the Server
```bash
python manage.py runserver
```

---

## 🔑 Administrative Account Details

For ease of testing, the seeding script creates a default superuser account:
- **URL**: `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 🧪 Running Automated Tests

To execute the view, redirection, and ID-generation test suite, run:
```bash
python manage.py test
```
