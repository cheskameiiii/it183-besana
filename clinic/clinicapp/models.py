from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid

# Existing models: Role, CustomUserManager, Account, Doctor, Patient

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.role

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    join_date = models.DateTimeField(default=timezone.now, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    last_login_date = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(Role, related_name='user_accounts')
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='user_accounts'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Doctor(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=1, null=True, blank=True)
    date_of_birth = models.DateField()
    email_address = models.EmailField(unique=True)
    specialist = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.last_name}, {self.first_name}"

class Patient(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=1, null=True, blank=True)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

# New Models

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Scheduled'
    )

    def __str__(self):
        return f"Appointment on {self.appointment_date} - {self.patient}"

class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)  # Example: "500mg"
    instructions = models.TextField(null=True, blank=True)  # Example: "Take twice daily after meals"

    def __str__(self):
        return self.name

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    medicines = models.ManyToManyField(Medicine, related_name='prescriptions')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for Appointment {self.appointment_id}"
