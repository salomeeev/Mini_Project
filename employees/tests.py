# pyrefly: ignore [missing-import]
from django.test import TestCase, Client
# pyrefly: ignore [missing-import]
from django.urls import reverse
from datetime import date
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User
from departments.models import Department
from designations.models import Designation
from employees.models import Employee

class EmployeeSystemTests(TestCase):
    def setUp(self):
        # Create department
        self.dept = Department.objects.create(name="QA Testing", description="Quality assurance")
        # Create designation
        self.desig = Designation.objects.create(name="QA Analyst", description="Tests software")
        # Create user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.client = Client()

    def test_employee_id_generation(self):
        # Create an employee and test auto-generated ID
        emp1 = Employee.objects.create(
            full_name="Test Dev 1",
            email="test1@example.com",
            phone="1234567890",
            department=self.dept,
            designation=self.desig,
            salary=60000.00,
            gender="Male",
            date_of_birth=date(1995, 1, 1),
            date_of_joining=date(2020, 1, 1),
            address="123 Street",
            city="City",
            state="State",
            country="Country",
            zip_code="12345"
        )
        self.assertEqual(emp1.employee_id, "EMP-00001")

        # Create another employee and test sequential auto-generated ID
        emp2 = Employee.objects.create(
            full_name="Test Dev 2",
            email="test2@example.com",
            phone="0987654321",
            department=self.dept,
            designation=self.desig,
            salary=70000.00,
            gender="Female",
            date_of_birth=date(1993, 2, 2),
            date_of_joining=date(2021, 2, 2),
            address="456 Road",
            city="Town",
            state="State",
            country="Country",
            zip_code="54321"
        )
        self.assertEqual(emp2.employee_id, "EMP-00002")

    def test_anonymous_user_redirected(self):
        # Accessing dashboard anonymously should redirect to login
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_authenticated_dashboard_access(self):
        # Login and access dashboard
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
