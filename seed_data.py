import os
import django
from datetime import date

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
django.setup()

from django.contrib.auth.models import User
from departments.models import Department
from designations.models import Designation
from employees.models import Employee

def seed_db():
    print("Starting database seeding...")

    # 1. Create Superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created successfully (username: admin, password: admin123)")
    else:
        print("Superuser 'admin' already exists.")

    # 2. Create Departments
    departments_data = [
        {"name": "Human Resources", "description": "Responsible for recruitment, training, payroll, and employee relations."},
        {"name": "Information Technology", "description": "Manages hardware, software, networking, and systems administration."},
        {"name": "Finance", "description": "Handles budgets, bookkeeping, accounting, financial reports, and auditing."},
        {"name": "Marketing", "description": "Handles brand management, public relations, advertising, and content creation."},
        {"name": "Operations", "description": "Manages day-to-day operations, supply chain logistics, and business processes."}
    ]

    depts = {}
    for d in departments_data:
        dept, created = Department.objects.get_or_create(name=d["name"], defaults={"description": d["description"]})
        depts[d["name"]] = dept
        if created:
            print(f"Department '{d['name']}' created.")

    # 3. Create Designations
    designations_data = [
        {"name": "HR Specialist", "description": "Focuses on recruitment and onboarding operations."},
        {"name": "HR Manager", "description": "Oversees the entire HR department operations."},
        {"name": "Software Engineer", "description": "Develops and maintains code for products and internal tools."},
        {"name": "Senior Software Architect", "description": "Designs core systems and software engineering patterns."},
        {"name": "Financial Analyst", "description": "Tracks expenditures, revenues, and projects financial forecasts."},
        {"name": "Marketing Coordinator", "description": "Manages content posting, analytics, and campaigns."},
        {"name": "Operations Director", "description": "Manages facility resources and logistical processes."}
    ]

    desigs = {}
    for d in designations_data:
        desig, created = Designation.objects.get_or_create(name=d["name"], defaults={"description": d["description"]})
        desigs[d["name"]] = desig
        if created:
            print(f"Designation '{d['name']}' created.")

    # 4. Create Sample Employees
    # Need at least 11 employees to showcase pagination (10 per page)
    employees_data = [
        {
            "full_name": "John Doe", "email": "john.doe@example.com", "phone": "9876543210",
            "department": depts["Information Technology"], "designation": desigs["Software Engineer"],
            "salary": 75000.00, "gender": "Male", "date_of_birth": date(1995, 5, 12), "date_of_joining": date(2021, 6, 1),
            "address": "123 Tech Park Ave", "city": "Seattle", "state": "Washington", "country": "USA", "zip_code": "98101",
            "status": "Active"
        },
        {
            "full_name": "Jane Smith", "email": "jane.smith@example.com", "phone": "8765432109",
            "department": depts["Human Resources"], "designation": desigs["HR Manager"],
            "salary": 85000.00, "gender": "Female", "date_of_birth": date(1990, 8, 24), "date_of_joining": date(2018, 3, 15),
            "address": "456 Oakwood Rd", "city": "Boston", "state": "Massachusetts", "country": "USA", "zip_code": "02108",
            "status": "Active"
        },
        {
            "full_name": "Alice Johnson", "email": "alice.j@example.com", "phone": "7654321098",
            "department": depts["Information Technology"], "designation": desigs["Senior Software Architect"],
            "salary": 135000.00, "gender": "Female", "date_of_birth": date(1985, 11, 3), "date_of_joining": date(2015, 10, 1),
            "address": "789 Pine Crest Dr", "city": "San Francisco", "state": "California", "country": "USA", "zip_code": "94102",
            "status": "Active"
        },
        {
            "full_name": "Robert Brown", "email": "robert.b@example.com", "phone": "6543210987",
            "department": depts["Finance"], "designation": desigs["Financial Analyst"],
            "salary": 68000.00, "gender": "Male", "date_of_birth": date(1993, 2, 18), "date_of_joining": date(2020, 1, 10),
            "address": "321 Wall Street Apt 4B", "city": "New York", "state": "New York", "country": "USA", "zip_code": "10005",
            "status": "Active"
        },
        {
            "full_name": "Emily Davis", "email": "emily.d@example.com", "phone": "5432109876",
            "department": depts["Marketing"], "designation": desigs["Marketing Coordinator"],
            "salary": 54000.00, "gender": "Female", "date_of_birth": date(1997, 7, 29), "date_of_joining": date(2022, 9, 1),
            "address": "555 Sunset Blvd", "city": "Los Angeles", "state": "California", "country": "USA", "zip_code": "90028",
            "status": "Active"
        },
        {
            "full_name": "Michael Wilson", "email": "michael.w@example.com", "phone": "4321098765",
            "department": depts["Operations"], "designation": desigs["Operations Director"],
            "salary": 98000.00, "gender": "Male", "date_of_birth": date(1982, 4, 15), "date_of_joining": date(2012, 5, 20),
            "address": "777 Industrial Way", "city": "Chicago", "state": "Illinois", "country": "USA", "zip_code": "60601",
            "status": "Active"
        },
        {
            "full_name": "David Martinez", "email": "david.m@example.com", "phone": "3210987654",
            "department": depts["Information Technology"], "designation": desigs["Software Engineer"],
            "salary": 72000.00, "gender": "Male", "date_of_birth": date(1996, 9, 30), "date_of_joining": date(2023, 2, 1),
            "address": "101 Silicon Valley Rd", "city": "San Jose", "state": "California", "country": "USA", "zip_code": "95101",
            "status": "Inactive"
        },
        {
            "full_name": "Sarah Garcia", "email": "sarah.g@example.com", "phone": "2109876543",
            "department": depts["Human Resources"], "designation": desigs["HR Specialist"],
            "salary": 58000.00, "gender": "Female", "date_of_birth": date(1994, 1, 5), "date_of_joining": date(2021, 11, 15),
            "address": "888 Maple Lane", "city": "Austin", "state": "Texas", "country": "USA", "zip_code": "78701",
            "status": "Active"
        },
        {
            "full_name": "James Taylor", "email": "james.t@example.com", "phone": "1098765432",
            "department": depts["Finance"], "designation": desigs["Financial Analyst"],
            "salary": 71000.00, "gender": "Male", "date_of_birth": date(1991, 12, 10), "date_of_joining": date(2019, 8, 1),
            "address": "404 Capital Court", "city": "Charlotte", "state": "North Carolina", "country": "USA", "zip_code": "28202",
            "status": "Active"
        },
        {
            "full_name": "Jessica Lee", "email": "jessica.l@example.com", "phone": "9988776655",
            "department": depts["Marketing"], "designation": desigs["Marketing Coordinator"],
            "salary": 56000.00, "gender": "Female", "date_of_birth": date(1998, 3, 22), "date_of_joining": date(2023, 7, 10),
            "address": "12 Broadway Ave", "city": "New York", "state": "New York", "country": "USA", "zip_code": "10003",
            "status": "Active"
        },
        {
            "full_name": "Kevin Thomas", "email": "kevin.t@example.com", "phone": "8877665544",
            "department": depts["Information Technology"], "designation": desigs["Software Engineer"],
            "salary": 76000.00, "gender": "Male", "date_of_birth": date(1994, 6, 17), "date_of_joining": date(2022, 1, 15),
            "address": "505 Redmond Way", "city": "Redmond", "state": "Washington", "country": "USA", "zip_code": "98052",
            "status": "Active"
        },
        {
            "full_name": "Lisa Anderson", "email": "lisa.a@example.com", "phone": "7766554433",
            "department": depts["Operations"], "designation": desigs["Operations Director"],
            "salary": 94000.00, "gender": "Female", "date_of_birth": date(1988, 10, 5), "date_of_joining": date(2017, 4, 1),
            "address": "909 Logistics Blvd", "city": "Atlanta", "state": "Georgia", "country": "USA", "zip_code": "30301",
            "status": "Inactive"
        }
    ]

    for emp_info in employees_data:
        emp, created = Employee.objects.get_or_create(email=emp_info["email"], defaults=emp_info)
        if created:
            print(f"Employee '{emp.full_name}' with ID '{emp.employee_id}' created.")

    print("Seeding finished successfully.")

if __name__ == '__main__':
    seed_db()
