from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Role, Account, Doctor, Patient, Appointment, Medicine, Prescription
from .forms import AppointmentForm, DoctorForm, PatientForm, MedicineForm, PrescriptionForm
from django.utils.timezone import now
from datetime import timedelta
import logging


class HealthcareAppTestCase(TestCase):

    def setUp(self):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Create a test role
        self.role = Role.objects.create(role="Doctor")

        # Create a test user account
        self.account = Account.objects.create_user(
            username="testuser",
            password="password",
            email="testuser@example.com",
            role=self.role
        )

        # Create a test doctor
        self.doctor = Doctor.objects.create(
            last_name="Smith",
            first_name="John",
            middle_initial="A",
            date_of_birth="1980-01-01",
            email_address="dr.smith@example.com",
            specialist="Cardiologist",
            gender="Male",
            contact_number="1234567890"
        )

        # Create a test patient
        self.patient = Patient.objects.create(
            last_name="Doe",
            first_name="Jane",
            middle_initial="B",
            age=30,
            date_of_birth="1993-01-01",
            gender="Female",
            contact_number="0987654321"
        )

        # Create a test appointment
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=now() + timedelta(days=1),
            reason="Routine Checkup",
            status="Scheduled"
        )

        # Create a test medicine
        self.medicine = Medicine.objects.create(
            name="Aspirin",
            dosage="500mg",
            instructions="Take one tablet after meals."
        )

        # Create a test prescription
        self.prescription = Prescription.objects.create(
            appointment=self.appointment,
            notes="Prescribed for headache."
        )
        self.prescription.medicines.add(self.medicine)

        # Set up the client
        self.client = Client()

    def test_doctor_creation(self):
        doctor = Doctor.objects.get(email_address="dr.smith@example.com")
        self.assertEqual(doctor.specialist, "Cardiologist")

    def test_patient_creation(self):
        patient = Patient.objects.get(contact_number="0987654321")
        self.assertEqual(patient.last_name, "Doe")

    def test_appointment_creation(self):
        appointment = Appointment.objects.get(reason="Routine Checkup")
        self.assertEqual(appointment.status, "Scheduled")

    def test_medicine_creation(self):
        medicine = Medicine.objects.get(name="Aspirin")
        self.assertEqual(medicine.dosage, "500mg")

    def test_prescription_creation(self):
        prescription = Prescription.objects.get(appointment=self.appointment)
        self.assertIn(self.medicine, prescription.medicines.all())

    def test_appointment_form(self):
        form_data = {
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'appointment_date': (now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S'),
            'reason': "Follow-up Checkup",
            'status': "Scheduled",
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_doctor_form(self):
        form_data = {
            'last_name': "Brown",
            'first_name': "Alice",
            'middle_initial': "C",
            'date_of_birth': "1985-05-05",
            'email_address': "dr.brown@example.com",
            'specialist': "Dermatologist",
            'gender': "Female",
            'contact_number': "1122334455",
        }
        form = DoctorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_patient_form(self):
        form_data = {
            'last_name': "Johnson",
            'first_name': "Michael",
            'middle_initial': "D",
            'age': 45,
            'date_of_birth': "1978-03-15",
            'gender': "Male",
            'contact_number': "2233445566",
        }
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_medicine_form(self):
        form_data = {
            'name': "Paracetamol",
            'dosage': "650mg",
            'instructions': "Take one tablet every 6 hours.",
        }
        form = MedicineForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_prescription_form(self):
        # Create a new appointment to test PrescriptionForm
        new_appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=now() + timedelta(days=2),
            reason="New Checkup",
            status="Scheduled"
        )
        
        form_data = {
            'appointment': new_appointment.appointment_id,  # Use the new appointment
            'medicines': [self.medicine.medicine_id],  # Correct field name
            'notes': "For fever and pain."
        }
        form = PrescriptionForm(data=form_data)
        if form.is_valid():
            self.logger.info("PrescriptionForm is valid.")
            self.assertTrue(form.is_valid())
        else:
            self.logger.error(f"PrescriptionForm errors: {form.errors}")
            self.fail(f"Form validation failed with errors: {form.errors}")
